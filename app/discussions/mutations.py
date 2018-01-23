import graphene

from app.discussions.models import Message, Reply
from app.discussions.types import (
    MessageType,
    ReplyType,
    MessageInputType,
    ReplyInputType
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


class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
    create_reply = CreateReplyMutation.Field()
