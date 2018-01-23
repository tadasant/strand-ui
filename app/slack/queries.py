import graphene

from app.slack.models import (
    SlackUser,
    SlackChannel,
    SlackTeam,
    SlackTeamInstallation,
)
from app.slack.types import (
    SlackUserType,
    SlackChannelType,
    SlackTeamType,
    SlackTeamInstallationType,
)


class Query(graphene.ObjectType):
    slack_user = graphene.Field(SlackUserType, id=graphene.String())
    slack_channel = graphene.Field(SlackChannelType, id=graphene.String())
    slack_team = graphene.Field(SlackTeamType, id=graphene.String())
    slack_team_installation = graphene.Field(SlackTeamInstallationType, id=graphene.Int())

    slack_users = graphene.List(SlackUserType)
    slack_channels = graphene.List(SlackChannelType)
    slack_teams = graphene.List(SlackTeamType)
    slack_team_installations = graphene.List(SlackTeamInstallationType)

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

    def resolve_slack_team_installation(self, info, id=None):
        if id is not None:
            return SlackTeamInstallation.objects.get(pk=id)

        return None

    def resolve_slack_users(self, info):
        return SlackUser.objects.all()

    def resolve_slack_channels(self, info):
        return SlackChannel.objects.all()

    def resolve_slack_teams(self, info):
        return SlackTeam.objects.all()

    def resolve_slack_team_installations(self, info):
        return SlackTeamInstallation.objects.all()
