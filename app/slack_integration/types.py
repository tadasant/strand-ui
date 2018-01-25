import graphene
from graphene_django.types import DjangoObjectType

from app.questions.types import SessionInputType, TagInputType
from app.slack_integration.models import (
    SlackChannel,
    SlackEvent,
    SlackTeam,
    SlackApplicationInstallation,
    SlackUser
)


class SlackChannelType(DjangoObjectType):
    class Meta:
        model = SlackChannel


class SlackEventType(DjangoObjectType):
    class Meta:
        model = SlackEvent


class SlackTeamType(DjangoObjectType):
    class Meta:
        model = SlackTeam


class SlackApplicationInstallationType(DjangoObjectType):
    class Meta:
        model = SlackApplicationInstallation


class SlackUserType(DjangoObjectType):
    class Meta:
        model = SlackUser


class SlackUserInputType(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    real_name = graphene.String(required=True)
    display_name = graphene.String(required=True)
    email = graphene.String()
    avatar_72 = graphene.String(required=True)
    is_bot = graphene.Boolean(required=True)
    is_admin = graphene.Boolean(required=True)
    slack_team_id = graphene.String(required=True)
    user_id = graphene.Int(required=True)


class SlackTeamInputType(graphene.InputObjectType):
    code = graphene.String(required=True)


class SlackChannelInputType(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    slack_team_id = graphene.String(required=True)
    session_id = graphene.Int(required=True)


class SlackApplicationInstallationInputType(graphene.InputObjectType):
    slack_team_id = graphene.String(required=True)
    access_token = graphene.String(required=True)
    scope = graphene.String(required=True)
    installer_id = graphene.String(required=True)
    bot_user_id = graphene.String(required=True)
    bot_access_token = graphene.String(required=True)


class SlackApplicationInstallationHelpChannelAndActivateInputType(graphene.InputObjectType):
    slack_team_id = graphene.String(required=True)
    help_channel_id = graphene.String(required=True)


class MessageFromSlackInputType(graphene.InputObjectType):
    origin_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    slack_user_id = graphene.String(required=True)
    text = graphene.String(required=True)
    time = graphene.String(required=True)


class ReplyFromSlackInputType(graphene.InputObjectType):
    message_origin_slack_event_ts = graphene.String(required=True)
    origin_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    slack_user_id = graphene.String(required=True)
    text = graphene.String(required=True)
    time = graphene.String(required=True)


class SessionFromSlackInputType(graphene.InputObjectType):
    session = graphene.Field(SessionInputType, required=True)
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    slack_team_id = graphene.String(required=True)


class UserFromSlackInputType(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    real_name = graphene.String(required=True)
    display_name = graphene.String(required=True)
    email = graphene.String()
    avatar_72 = graphene.String(required=True)
    is_bot = graphene.Boolean(required=True)
    is_admin = graphene.Boolean(required=True)
    slack_team_id = graphene.String(required=True)


class UserAndMessageFromSlackInputType(graphene.InputObjectType):
    slack_user = graphene.Field(UserFromSlackInputType)
    origin_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    text = graphene.String(required=True)
    time = graphene.String(required=True)


class UserAndReplyFromSlackInputType(graphene.InputObjectType):
    slack_user = graphene.Field(UserFromSlackInputType)
    message_origin_slack_event_ts = graphene.String(required=True)
    origin_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    text = graphene.String(required=True)
    time = graphene.String(required=True)


class GroupFromSlackInputType(graphene.InputObjectType):
    slack_team_id = graphene.String(required=True)
    slack_team_name = graphene.String(required=True)
    group_name = graphene.String(required=True)


class SolveQuestionFromSlackInputType(graphene.InputObjectType):
    slack_channel_id = graphene.String()
    slack_user_id = graphene.String()
    time_end = graphene.String()


class QuestionFromSlackInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_solved = graphene.Boolean()
    is_anonymous = graphene.Boolean()
    original_poster_slack_user_id = graphene.String(required=True)
    tags = graphene.List(TagInputType)


class UserAndQuestionFromSlackInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_solved = graphene.Boolean()
    is_anonymous = graphene.Boolean()
    original_poster_slack_user = graphene.Field(UserFromSlackInputType)
    tags = graphene.List(TagInputType)
