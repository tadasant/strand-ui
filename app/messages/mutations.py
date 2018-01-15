import graphene

from app.messages.models import Message, Reply, SlackEvent
from app.messages.types import MessageType, ReplyType, MessageInputType, ReplyInputType


class CreateMessageMutation(graphene.Mutation):
    class Arguments:
        input = MessageInputType(required=True)

    message = graphene.Field(MessageType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        message = Message.objects.create(**input)
        return CreateMessageMutation(message=message)


class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
