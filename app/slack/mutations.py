import graphene
from app.slack.types import (
    SlackUserType,
    SlackUserInputType,
    SlackTeamType,
    SlackTeamInputType,
    SlackChannelType,
    SlackChannelInputType,
    SlackSettingsType,
    SlackSettingsInputType
)
from app.slack.models import SlackTeam, SlackUser, SlackChannel, SlackSettings
from app.users.models import User
from app.groups.models import Group
from app.questions.models import Session


class CreateSlackUserMutation(graphene.Mutation):
    class Arguments:
        input = SlackUserInputType(required=True)

    slack_user = graphene.Field(SlackUserType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        if not User.objects.filter(pk=input.user_id).exists():
            raise Exception('Invalid User Id')

        slack_user = SlackUser.objects.create(**input)
        return CreateSlackUserMutation(slack_user=slack_user)


class CreateSlackTeamMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamInputType(required=True)

    slack_team = graphene.Field(SlackTeamType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not Group.objects.filter(pk=input.group_id).exists():
            raise Exception('Invalid Group Id')

        slack_team = SlackTeam.objects.create(**input)
        return CreateSlackTeamMutation(slack_team=slack_team)


class CreateSlackChannelMutation(graphene.Mutation):
    class Arguments:
        input = SlackChannelInputType(required=True)

    slack_channel = graphene.Field(SlackChannelType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        if not Session.objects.filter(pk=input.session_id).exists():
            raise Exception('Invalid Session Id')

        slack_channel = SlackChannel.objects.create(**input)
        return CreateSlackChannelMutation(slack_channel=slack_channel)


class CreateSlackSettingsMutation(graphene.Mutation):
    class Arguments:
        input = SlackSettingsInputType(required=True)

    slack_settings = graphene.Field(SlackSettingsType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        slack_settings = SlackSettings.objects.create(**input)
        return CreateSlackSettingsMutation(slack_settings=slack_settings)


class Mutation(graphene.ObjectType):
    create_slack_user = CreateSlackUserMutation.Field()
    create_slack_team = CreateSlackTeamMutation.Field()
    create_slack_channel = CreateSlackChannelMutation.Field()
    create_slack_settings = CreateSlackSettingsMutation.Field()
