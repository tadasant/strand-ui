import graphene
from graphene_django.types import DjangoObjectType

from app.questions.models import Question, Session, Tag


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class SessionType(DjangoObjectType):
    class Meta:
        model = Session


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class TagInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class QuestionInputType(graphene.InputObjectType):
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
    question_id = graphene.Int(required=True)


class QuestionAndTagsInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_solved = graphene.Boolean()
    is_anonymous = graphene.Boolean()
    original_poster_id = graphene.Int(required=True)
    solver_id = graphene.Int()
