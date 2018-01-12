import graphene
from graphene_django.types import DjangoObjectType

from app.questions.models import Question, Tag, Session


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class SessionType(DjangoObjectType):
    class Meta:
        model = Session


class Query(graphene.ObjectType):
    question = graphene.Field(QuestionType, id=graphene.Int())
    tag = graphene.Field(TagType, name=graphene.String())
    session = graphene.Field(SessionType, id=graphene.Int())

    questions = graphene.List(QuestionType)
    tags = graphene.List(TagType)
    sessions = graphene.List(SessionType)

    def resolve_question(self, info, id=None):
        if id is not None:
            return Question.objects.get(pk=id)

        return None

    def resolve_tag(self, info, name=None):
        if name is not None:
            return Tag.objects.get(name=name)

        return None

    def resolve_session(self, info, id=None):
        if id is not None:
            return Session.objects.get(pk=id)

        return None

    def resolve_questions(self, info):
        return Question.objects.all()

    def resolve_tags(self, info):
        return Tag.objects.all()

    def resolve_sessions(self, info):
        return Session.objects.all()
