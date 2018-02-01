import graphene

from app.topics.models import Topic, Discussion, Tag
from app.topics.types import TopicType, DiscussionType, TagType


class Query(graphene.ObjectType):
    topic = graphene.Field(TopicType, id=graphene.Int())
    tag = graphene.Field(TagType, name=graphene.String())
    discussion = graphene.Field(DiscussionType, id=graphene.Int())

    topics = graphene.List(TopicType)
    tags = graphene.List(TagType)
    discussions = graphene.List(DiscussionType)

    def resolve_topic(self, info, id=None):
        if id is not None:
            return Topic.objects.get(pk=id)

        return None

    def resolve_tag(self, info, name=None):
        if name is not None:
            return Tag.objects.get(name=name)

        return None

    def resolve_discussion(self, info, id=None):
        if id is not None:
            return Discussion.objects.get(pk=id)

        return None

    def resolve_topics(self, info):
        return Topic.objects.all()

    def resolve_tags(self, info):
        return Tag.objects.all()

    def resolve_discussions(self, info):
        return Discussion.objects.all()
