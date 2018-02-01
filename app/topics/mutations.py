import graphene

from app.api.authorization import check_authorization
from app.topics.models import Topic
from app.topics.validators import TopicValidator, SessionValidator, TagValidator
from app.topics.types import (
    TopicType,
    TopicInputType,
    SessionType,
    SessionInputType,
    SolveTopicInputType,
    TagType,
    TagInputType
)
from app.users.models import User


class CreateTopicMutation(graphene.Mutation):
    class Arguments:
        input = TopicInputType(required=True)

    topic = graphene.Field(TopicType)

    @check_authorization
    def mutate(self, info, input):
        tags = input.pop('tags', [])

        topic_validator = TopicValidator(data=input)
        topic_validator.is_valid(raise_exception=True)
        topic = topic_validator.save()

        topic.add_or_create_tags(tags)

        return CreateTopicMutation(topic=topic)


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


class SolveTopicMutation(graphene.Mutation):
    class Arguments:
        input = SolveTopicInputType(required=True)

    topic = graphene.Field(TopicType)
    session = graphene.Field(SessionType)

    @check_authorization
    def mutate(self, info, input):
        topic = Topic.objects.get(pk=input['id'])
        solver = User.objects.get(pk=input['solver_id'])

        topic.session.mark_as_closed()
        topic.session.save()

        topic.mark_as_solved()
        topic.solver = solver
        topic.save()

        return SolveTopicMutation(topic=topic, session=topic.session)


class Mutation(graphene.ObjectType):
    create_topic = CreateTopicMutation.Field()
    create_session = CreateSessionMutation.Field()
    create_tag = CreateTagMutation.Field()

    solve_topic = SolveTopicMutation.Field()
