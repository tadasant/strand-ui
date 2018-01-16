import graphene
from graphene_django.types import DjangoObjectType

from app.questions.types import SessionInputType
from app.slack.models import SlackUser, SlackChannel, SlackTeam, SlackSettings, SlackEvent


class SlackChannelType(DjangoObjectType):
    class Meta:
        model = SlackChannel


class SlackEventType(DjangoObjectType):
    class Meta:
        model = SlackEvent


class SlackSettingsType(DjangoObjectType):
    class Meta:
        model = SlackSettings


class SlackTeamType(DjangoObjectType):
    class Meta:
        model = SlackTeam


class SlackUserType(DjangoObjectType):
    class Meta:
        model = SlackUser


class SlackUserInputType(graphene.InputObjectType):
    id = graphene.String(required=True)
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
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    group_id = graphene.Int(required=True)


class SlackChannelInputType(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    slack_team_id = graphene.String(required=True)
    session_id = graphene.Int(required=True)


class SlackSettingsInputType(graphene.InputObjectType):
    bot_token = graphene.String()
    slack_team_id = graphene.String(required=True)


class SlackEventAndMessageInputType(graphene.InputObjectType):
    text = graphene.String(required=True)
    time = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    slack_user_id = graphene.String(required=True)
    slack_event_ts = graphene.String(required=True)


class SlackEventAndReplyInputType(graphene.InputObjectType):
    text = graphene.String(required=True)
    time = graphene.String(required=True)
    message_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    slack_user_id = graphene.String(required=True)
    slack_event_ts = graphene.String(required=True)


class SessionAndSlackChannelInputType(graphene.InputObjectType):
    session = graphene.Field(SessionInputType, required=True)
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    slack_team_id = graphene.String(required=True)
