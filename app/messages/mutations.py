import graphene

from app.messages.models import Message, Reply, SlackEvent
from app.messages.types import (
    MessageType,
    ReplyType,
    MessageInputType,
    ReplyInputType,
    MessageAndSlackEventInputType,
    ReplyAndSlackEventInputType
)


class CreateMessageMutation(graphene.Mutation):
    class Arguments:
        input = MessageInputType(required=True)

    message = graphene.Field(MessageType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        message = Message.objects.create(**input)
        return CreateMessageMutation(message=message)


class CreateReplyMutation(graphene.Mutation):
    class Arguments:
        input = ReplyInputType(required=True)

    reply = graphene.Field(ReplyType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        reply = Reply.objects.create(**input)
        return CreateReplyMutation(reply=reply)


class CreateMessageAndSlackEventMutation(graphene.Mutation):
    class Arguments:
        input = MessageAndSlackEventInputType(required=True)

    message = graphene.Field(MessageType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        timestamp = input.pop('slack_event_timestamp')
        slack_event = SlackEvent.objects.create(timestamp=timestamp)

        message = Message.objects.create(**input)
        message.slack_event = slack_event
        message.save()

        return CreateMessageAndSlackEventMutation(message=message)


class CreateReplyAndSlackEventMutation(graphene.Mutation):
    class Arguments:
        input = ReplyAndSlackEventInputType(required=True)

    reply = graphene.Field(ReplyType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        timestamp = input.pop('slack_event_timestamp')
        slack_event = SlackEvent.objects.create(timestamp=timestamp)

        reply = Reply.objects.create(**input)
        reply.slack_event = slack_event
        reply.save()

        return CreateReplyAndSlackEventMutation(reply=reply)


class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
    create_reply = CreateReplyMutation.Field()
    create_message_and_slack_event = CreateMessageAndSlackEventMutation.Field()
    create_reply_and_slack_event = CreateReplyAndSlackEventMutation.Field()
