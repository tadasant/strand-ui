import graphene

from app.api.authorization import check_authorization
from app.questions.models import Question
from app.questions.validators import QuestionValidator, SessionValidator, TagValidator
from app.questions.types import (
    QuestionType,
    QuestionInputType,
    SessionType,
    SessionInputType,
    SolveQuestionInputType,
    TagType,
    TagInputType
)
from app.users.models import User


class CreateQuestionMutation(graphene.Mutation):
    class Arguments:
        input = QuestionInputType(required=True)

    question = graphene.Field(QuestionType)

    @check_authorization
    def mutate(self, info, input):
        tags = input.pop('tags', [])

        question_validator = QuestionValidator(data=input)
        question_validator.is_valid(raise_exception=True)
        question = question_validator.save()

        question.add_or_create_tags(tags)

        return CreateQuestionMutation(question=question)


class CreateSessionMutation(graphene.Mutation):
    class Arguments:
        input = SessionInputType(required=True)

    session = graphene.Field(SessionType)

    @check_authorization
    def mutate(self, info, input):
        session_validator = SessionValidator(data=input)
        session_validator.is_valid(raise_exception=True)
        session = session_validator.save()

        return CreateSessionMutation(session=session)


class CreateTagMutation(graphene.Mutation):
    class Arguments:
        input = TagInputType(required=True)

    tag = graphene.Field(TagType)

    @check_authorization
    def mutate(self, info, input):
        tag_validator = TagValidator(data=input)
        tag_validator.is_valid(raise_exception=True)
        tag = tag_validator.save()

        return CreateTagMutation(tag=tag)


class SolveQuestionMutation(graphene.Mutation):
    class Arguments:
        input = SolveQuestionInputType(required=True)

    question = graphene.Field(QuestionType)
    session = graphene.Field(SessionType)

    @check_authorization
    def mutate(self, info, input):
        question = Question.objects.get(pk=input['id'])
        solver = User.objects.get(pk=input['solver_id'])

        question.session.mark_as_closed()
        question.session.save()

        question.mark_as_solved()
        question.solver = solver
        question.save()

        return SolveQuestionMutation(question=question, session=question.session)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestionMutation.Field()
    create_session = CreateSessionMutation.Field()
    create_tag = CreateTagMutation.Field()

    solve_question = SolveQuestionMutation.Field()
