import graphene

from app.questions.models import Question, Session, Tag
from app.questions.types import (
    QuestionType,
    QuestionInputType,
    SessionType,
    SessionInputType,
    TagType,
    TagInputType
)


class CreateQuestionMutation(graphene.Mutation):
    class Arguments:
        input = QuestionInputType(required=True)

    question = graphene.Field(QuestionType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        question = Question.objects.create(**input)
        return CreateQuestionMutation(question=question)


class CreateSessionMutation(graphene.Mutation):
    class Arguments:
        input = SessionInputType(required=True)

    session = graphene.Field(SessionType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        session = Session.objects.create(**input)
        return CreateSessionMutation(session=session)


class CreateTagMutation(graphene.Mutation):
    class Arguments:
        input = TagInputType(required=True)

    tag = graphene.Field(TagType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        tag = Tag.objects.create(**input)
        return CreateTagMutation(tag=tag)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestionMutation.Field()
    create_session = CreateSessionMutation.Field()
    create_tag = CreateTagMutation.Field()
