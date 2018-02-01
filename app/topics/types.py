import graphene
from graphene_django.types import DjangoObjectType

from app.topics.models import Topic, Session, Tag


class TopicType(DjangoObjectType):
    class Meta:
        model = Topic


class SessionType(DjangoObjectType):
    class Meta:
        model = Session


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class TagInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class TopicInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_solved = graphene.Boolean()
    is_anonymous = graphene.Boolean()
    original_poster_id = graphene.Int(required=True)
    solver_id = graphene.Int()
    group_id = graphene.Int()
    tags = graphene.List(TagInputType)


class SessionInputType(graphene.InputObjectType):
    time_start = graphene.String()
    time_end = graphene.String()
    topic_id = graphene.Int(required=True)


class TopicAndTagsInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_solved = graphene.Boolean()
    is_anonymous = graphene.Boolean()
    original_poster_id = graphene.Int(required=True)
    solver_id = graphene.Int()


class SolveTopicInputType(graphene.InputObjectType):
    id = graphene.Int()
    solver_id = graphene.Int()
