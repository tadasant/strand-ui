import graphene

from app.topics.models import Topic, Session, Tag
from app.topics.types import TopicType, SessionType, TagType


class Query(graphene.ObjectType):
    topic = graphene.Field(TopicType, id=graphene.Int())
    tag = graphene.Field(TagType, name=graphene.String())
    session = graphene.Field(SessionType, id=graphene.Int())

    topics = graphene.List(TopicType)
    tags = graphene.List(TagType)
    sessions = graphene.List(SessionType)

    def resolve_topic(self, info, id=None):
        if id is not None:
            return Topic.objects.get(pk=id)

        return None

    def resolve_tag(self, info, name=None):
        if name is not None:
            return Tag.objects.get(name=name)

        return None

    def resolve_session(self, info, id=None):
        if id is not None:
            return Session.objects.get(pk=id)

        return None

    def resolve_topics(self, info):
        return Topic.objects.all()

    def resolve_tags(self, info):
        return Tag.objects.all()

    def resolve_sessions(self, info):
        return Session.objects.all()
