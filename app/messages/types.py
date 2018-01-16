import graphene
from graphene_django.types import DjangoObjectType

from app.messages.models import Message, Reply


class MessageType(DjangoObjectType):
    class Meta:
        model = Message


class ReplyType(DjangoObjectType):
    class Meta:
        model = Reply


class MessageInputType(graphene.InputObjectType):
    text = graphene.String(required=True)
    session_id = graphene.Int(required=True)
    author_id = graphene.Int(required=True)
    time = graphene.String(required=True)
    slack_event_id = graphene.Int()


class ReplyInputType(graphene.InputObjectType):
    text = graphene.String(required=True)
    message_id = graphene.Int(required=True)
    author_id = graphene.Int(required=True)
    time = graphene.String(required=True)
    slack_event_id = graphene.Int()
