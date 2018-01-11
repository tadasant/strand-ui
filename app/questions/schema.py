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


class Query(object):
    question = graphene.Field(QuestionType, id=graphene.Int())
    tag = graphene.Field(TagType, name=graphene.String())
    session = graphene.Field(SessionType, id=graphene.Int())

    all_questions = graphene.List(QuestionType)
    all_tags = graphene.List(TagType)
    all_sessions = graphene.List(SessionType)

    def resolve_question(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Question.objects.get(pk=id)

        return None

    def resolve_tag(self, info, **kwargs):
        name = kwargs.get('name')

        if id is not None:
            return Tag.objects.get(name=name)

        return None

    def resolve_session(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Session.objects.get(pk=id)

        return None

    def resolve_all_questions(self, info, **kwargs):
        return Question.objects.all()

    def resolve_all_tags(self, info, **kwargs):
        return Tag.objects.all()

    def resolve_all_sessions(self, info, **kwargs):
        return Session.objects.all()
