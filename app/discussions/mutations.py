import graphene

from app.discussions.validators import MessageValidator, ReplyValidator
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
        message_validator = MessageValidator(data=input)
        message_validator.is_valid(raise_exception=True)
        message = message_validator.save()
        return CreateMessageMutation(message=message)


class CreateReplyMutation(graphene.Mutation):
    class Arguments:
        input = ReplyInputType(required=True)

    reply = graphene.Field(ReplyType)

    def mutate(self, info, input):
        reply_validator = ReplyValidator(data=input)
        reply_validator.is_valid(raise_exception=True)
        reply = reply_validator.save()
        return CreateReplyMutation(reply=reply)


class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
    create_reply = CreateReplyMutation.Field()
