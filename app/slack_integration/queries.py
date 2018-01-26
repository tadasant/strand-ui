import graphene

from app.slack_integration.models import (
    SlackUser,
    SlackChannel,
    SlackTeam,
    SlackApplicationInstallation,
    SlackAgent
)
from app.slack_integration.types import (
    SlackUserType,
    SlackChannelType,
    SlackTeamType,
    SlackApplicationInstallationType,
    SlackAgentType
)


class Query(graphene.ObjectType):
    slack_agent = graphene.Field(SlackAgentType, id=graphene.String())
    slack_user = graphene.Field(SlackUserType, id=graphene.String())
    slack_channel = graphene.Field(SlackChannelType, id=graphene.String())
    slack_team = graphene.Field(SlackTeamType, id=graphene.String())
    slack_application_installation = graphene.Field(SlackApplicationInstallationType, id=graphene.Int())

    slack_agents = graphene.List(SlackAgentType)
    slack_users = graphene.List(SlackUserType)
    slack_channels = graphene.List(SlackChannelType)
    slack_teams = graphene.List(SlackTeamType)
    slack_application_installations = graphene.List(SlackApplicationInstallationType)

    def resolve_slack_agent(self, info, id=None):
        if id is not None:
            return SlackAgent.objects.get(pk=id)
        return None

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

    def resolve_slack_application_installation(self, info, id=None):
        return SlackApplicationInstallation.objects.get(pk=id)

    def resolve_slack_agents(self, info):
        return SlackAgent.objects.all()

    def resolve_slack_users(self, info):
        return SlackUser.objects.all()

    def resolve_slack_channels(self, info):
        return SlackChannel.objects.all()

    def resolve_slack_teams(self, info):
        return SlackTeam.objects.all()

    def resolve_slack_application_installations(self, info):
        return SlackApplicationInstallation.objects.all()
