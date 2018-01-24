import graphene
from graphene_django.types import DjangoObjectType

from app.questions.types import SessionInputType
from app.slack_integration.models import (
    SlackChannel,
    SlackEvent,
    SlackTeam,
    SlackTeamInstallation,
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


class SlackTeamInstallationType(DjangoObjectType):
    class Meta:
        model = SlackTeamInstallation


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
    avatar_72 = graphene.String()
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


class SlackTeamInstallationInputType(graphene.InputObjectType):
    slack_team_id = graphene.String(required=True)
    access_token = graphene.String(required=True)
    scope = graphene.String(required=True)
    installer_id = graphene.String(required=True)
    bot_user_id = graphene.String(required=True)
    bot_access_token = graphene.String(required=True)


class SlackTeamInstallationHelpChannelAndActivateInputType(graphene.InputObjectType):
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
    avatar_72 = graphene.String()
    is_bot = graphene.Boolean(required=True)
    is_admin = graphene.Boolean(required=True)
    slack_team_id = graphene.String(required=True)


class GroupFromSlackInputType(graphene.InputObjectType):
    slack_team_id = graphene.String(required=True)
    slack_team_name = graphene.String(required=True)
    group_name = graphene.String(required=True)


class SolveQuestionFromSlackInputType(graphene.InputObjectType):
    slack_channel_id = graphene.String()
    slack_user_id = graphene.String()
    time_end = graphene.String()


class UserAndMessageFromSlackInputType(graphene.InputObjectType):
    slack_user = graphene.Field(UserFromSlackInputType)
    origin_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    text = graphene.String(required=True)
    time = graphene.String(required=True)
