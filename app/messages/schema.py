import graphene
from graphene_django.types import DjangoObjectType

from app.messages.models import Message, Reply


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class ReplyType(DjangoObjectType):
    class Meta:
        model = Reply


class Query(object):
    message = graphene.Field(MessageType, id=graphene.Int())
    reply = graphene.Field(ReplyType, id=graphene.Int())

    all_messages = graphene.List(MessageType)
    all_replies = graphene.List(ReplyType)

    def resolve_message(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Message.objects.get(pk=id)

        return None

    def resolve_reply(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Reply.objects.get(pk=id)

        return None

    def resolve_all_messages(self, info, **kwargs):
        return Message.objects.all()

    def resolve_all_replies(self, info, **kwargs):
        return Reply.objects.all()
