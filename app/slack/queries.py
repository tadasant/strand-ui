import graphene

from app.slack.models import SlackUser, SlackChannel, SlackTeam, SlackSettings
from app.slack.types import SlackUserType, SlackChannelType, SlackTeamType, SlackSettingsType


class Query(graphene.ObjectType):
    slack_user = graphene.Field(SlackUserType, id=graphene.String())
    slack_channel = graphene.Field(SlackChannelType, id=graphene.String())
    slack_team = graphene.Field(SlackTeamType, id=graphene.String())
    slack_settings = graphene.Field(SlackSettingsType, id=graphene.Int())

    slack_users = graphene.List(SlackUserType)
    slack_channels = graphene.List(SlackChannelType)
    slack_teams = graphene.List(SlackTeamType)
    slacks_settings = graphene.List(SlackSettingsType)

    def resolve_slack_user(self, info, id=None):
        if id is not None:
            return SlackUser.objects.get(pk=id)

        return None

    def resolve_slack_channel(self, info, id=None):
        if id is not None:
            return SlackChannel.objects.get(pk=id)

        return None

    def resolve_slack_team(self, info, id=None):
        if id is not None:
            return SlackTeam.objects.get(pk=id)

        return None

    def resolve_slack_settings(self, info, id=None):
        if id is not None:
            return SlackSettings.objects.get(pk=id)

        return None

    def resolve_slack_users(self, info):
        return SlackUser.objects.all()

    def resolve_slack_channels(self, info):
        return SlackChannel.objects.all()

    def resolve_slack_teams(self, info):
        return SlackTeam.objects.all()

    def resolve_slacks_settings(self, info):
        return SlackSettings.objects.all()
