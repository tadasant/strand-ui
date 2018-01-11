import graphene
from graphene_django.types import DjangoObjectType

from app.slack.models import SlackUser, SlackChannel, SlackTeam, SlackSettings


class SlackUserType(DjangoObjectType):
    class Meta:
        model = SlackUser


class SlackChannelType(DjangoObjectType):
    class Meta:
        model = SlackChannel


class SlackTeamType(DjangoObjectType):
    class Meta:
        model = SlackTeam


class SlackSettingsType(DjangoObjectType):
    class Meta:
        model = SlackSettings


class Query(object):
    slack_user = graphene.Field(SlackUserType, id=graphene.String())
    slack_channel = graphene.Field(SlackChannelType, id=graphene.String())
    slack_team = graphene.Field(SlackTeamType, id=graphene.String())
    slack_settings = graphene.Field(SlackSettingsType, id=graphene.Int())

    all_slack_users = graphene.List(SlackUserType)
    all_slack_channels = graphene.List(SlackChannelType)
    all_slack_teams = graphene.List(SlackTeamType)
    all_slack_settings = graphene.List(SlackSettingsType)

    def resolve_slack_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return SlackUser.objects.get(pk=id)

        return None

    def resolve_slack_channel(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return SlackChannel.objects.get(pk=id)

        return None

    def resolve_slack_team(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return SlackTeam.objects.get(pk=id)

        return None

    def resolve_slack_settings(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return SlackSettings.objects.get(pk=id)

        return None

    def resolve_all_slack_users(self, info, **kwargs):
        return SlackUser.objects.all()

    def resolve_all_slack_channels(self, info, **kwargs):
        return SlackChannel.objects.all()

    def resolve_all_slack_teams(self, info, **kwargs):
        return SlackTeam.objects.all()

    def resolve_all_slack_settings(self, info, **kwargs):
        return SlackSettings.objects.all()