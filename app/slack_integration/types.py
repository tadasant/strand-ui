import graphene
from graphene_django.types import DjangoObjectType

from app.api.authorization import check_authorization
from app.slack_integration.models import (
    SlackAgent,
    SlackChannel,
    SlackEvent,
    SlackTeam,
    SlackApplicationInstallation,
    SlackUser
)
from app.topics.types import DiscussionInputType, TagInputType


class SlackAgentType(DjangoObjectType):
    class Meta:
        model = SlackAgent


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

    @check_authorization
    def resolve_access_token(self, info):
        return self.access_token

    @check_authorization
    def resolve_bot_user_id(self, info):
        return self.bot_user_id

    @check_authorization
    def resolve_bot_access_token(self, info):
        return self.bot_access_token

    @check_authorization
    def resolve_installer(self, info):
        return self.installer

    @check_authorization
    def resolve_scope(self, info):
        return self.scope

    @check_authorization
    def resolve_slack_agent(self, info):
        return self.slack_agent


class SlackUserType(DjangoObjectType):
    class Meta:
        model = SlackUser
        only_fields = ('id', 'display_name', 'slack_team', 'user')

    @check_authorization
    def resolve_id(self, info):
        return self.id

    @check_authorization
    def resolve_slack_team(self, info):
        return self.slack_team

    @check_authorization
    def resolve_display_name(self, info):
        return self.display_name

    @check_authorization
    def resolve_user(self, info):
        return self.user


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


class SlackAgentInputType(graphene.InputObjectType):
    code = graphene.String(required=True)


class SlackChannelInputType(graphene.InputObjectType):
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    slack_team_id = graphene.String(required=True)
    discussion_id = graphene.Int(required=True)


class SlackAgentTopicChannelAndActivateInputType(graphene.InputObjectType):
    slack_team_id = graphene.String(required=True)
    topic_channel_id = graphene.String(required=True)


class MessageFromSlackInputType(graphene.InputObjectType):
    origin_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    slack_user_id = graphene.String(required=True)
    text = graphene.String(required=True)


class ReplyFromSlackInputType(graphene.InputObjectType):
    message_origin_slack_event_ts = graphene.String(required=True)
    origin_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    slack_user_id = graphene.String(required=True)
    text = graphene.String(required=True)


class DiscussionFromSlackInputType(graphene.InputObjectType):
    discussion = graphene.Field(DiscussionInputType, required=True)
    id = graphene.String(required=True)
    name = graphene.String(required=True)
    slack_team_id = graphene.String(required=True)


class MarkDiscussionAsPendingClosedFromSlackInputType(graphene.InputObjectType):
    slack_channel_id = graphene.String(required=True)


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


class UserAndReplyFromSlackInputType(graphene.InputObjectType):
    slack_user = graphene.Field(UserFromSlackInputType)
    message_origin_slack_event_ts = graphene.String(required=True)
    origin_slack_event_ts = graphene.String(required=True)
    slack_channel_id = graphene.String(required=True)
    text = graphene.String(required=True)


class GroupFromSlackInputType(graphene.InputObjectType):
    slack_team_id = graphene.String(required=True)
    slack_team_name = graphene.String(required=True)
    group_name = graphene.String(required=True)


class CloseDiscussionFromSlackInputType(graphene.InputObjectType):
    slack_channel_id = graphene.String(required=True)
    slack_user_id = graphene.String(required=True)
    time_end = graphene.String()


class TopicFromSlackInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_anonymous = graphene.Boolean()
    original_poster_slack_user_id = graphene.String(required=True)
    tags = graphene.List(TagInputType)


class UserAndTopicFromSlackInputType(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    is_anonymous = graphene.Boolean()
    original_poster_slack_user = graphene.Field(UserFromSlackInputType)
    tags = graphene.List(TagInputType)
