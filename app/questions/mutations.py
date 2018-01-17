import graphene

from app.questions.models import Question, Session, Tag
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

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not User.objects.filter(pk=input['original_poster_id']).exists():
            raise Exception('Invalid User Id')

        question_tags = input.pop('tags', [])
        question = Question.objects.create(**input)

        for question_tag in question_tags:
            tag, created = Tag.objects.get_or_create(name=question_tag['name'])
            question.tags.add(tag)

        return CreateQuestionMutation(question=question)


class CreateSessionMutation(graphene.Mutation):
    class Arguments:
        input = SessionInputType(required=True)

    session = graphene.Field(SessionType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not Question.objects.filter(pk=input['question_id']).exists():
            raise Exception('Invalid Question Id')

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


class SolveQuestionMutation(graphene.Mutation):
    class Arguments:
        input = SolveQuestionInputType(required=True)

    question = graphene.Field(QuestionType)
    session = graphene.Field(SessionType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not Question.objects.filter(pk=input['question_id']).exists():
            raise Exception('Invalid Question Id')

        if not User.objects.filter(pk=input['solver_id']).exists():
            raise Exception('Invalid User Id')

        question = Question.objects.get(pk=input['question_id'])
        question.is_solved = True
        question.solver_id = input['solver_id']
        question.save()

        session = question.session
        session.time_end = input['time_end']
        session.save()

        return SolveQuestionMutation(question=question, session=session)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestionMutation.Field()
    create_session = CreateSessionMutation.Field()
    create_tag = CreateTagMutation.Field()

    solve_question = SolveQuestionMutation.Field()
