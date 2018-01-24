import graphene

from app.discussions.models import Message, Reply
from app.discussions.serializers import MessageSerializer, ReplySerializer
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

        message_serializer = MessageSerializer(data=input)
        message_serializer.is_valid(raise_exception=True)
        message = message_serializer.save()
        return CreateMessageMutation(message=message)


class CreateReplyMutation(graphene.Mutation):
    class Arguments:
        input = ReplyInputType(required=True)

    reply = graphene.Field(ReplyType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        reply_serializer = ReplySerializer(data=input)
        reply_serializer.is_valid(raise_exception=True)
        reply = reply_serializer.save()
        return CreateReplyMutation(reply=reply)


class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
    create_reply = CreateReplyMutation.Field()
