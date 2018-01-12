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

    status = graphene.Int()
    form_errors = graphene.String()
    slack_user = graphene.Field(SlackUserType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return CreateSlackUserMutation(status=403,
                                           form_errors={'message': ['Unauthorized']})

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            return CreateSlackUserMutation(status=400,
                                           form_errors={'message': ['Invalid Slack Team Id']})
        if not User.objects.filter(pk=input.user_id).exists():
            return CreateSlackUserMutation(status=400,
                                           form_errors={'message': ['Invalid User Id']})

        slack_user = SlackUser.objects.create(**input)
        return CreateSlackUserMutation(slack_user=slack_user, status=201)


class CreateSlackTeamMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamInputType(required=True)

    status = graphene.Int()
    form_errors = graphene.String()
    slack_team = graphene.Field(SlackTeamType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return CreateSlackTeamMutation(status=403,
                                           form_errors={'message': ['Unauthorized']})

        if not Group.objects.filter(pk=input.group_id).exists():
            return CreateSlackTeamMutation(status=400,
                                           form_errors={'message': ['Invalid Group Id']})

        slack_team = SlackTeam.objects.create(**input)
        return CreateSlackTeamMutation(slack_team=slack_team, status=201)


class CreateSlackChannelMutation(graphene.Mutation):
    class Arguments:
        input = SlackChannelInputType(required=True)

    status = graphene.Int()
    form_errors = graphene.String()
    slack_channel = graphene.Field(SlackChannelType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return CreateSlackChannelMutation(status=403,
                                              form_errors={'message': ['Unauthorized']})

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            return CreateSlackChannelMutation(status=400,
                                              form_errors={'message': ['Invalid Slack Team Id']})

        if not Session.objects.filter(pk=input.session_id).exists():
            return CreateSlackChannelMutation(status=400,
                                              form_errors={'message': ['Invalid Session Id']})

        slack_channel = SlackChannel.objects.create(**input)
        return CreateSlackChannelMutation(slack_channel=slack_channel, status=201)


class CreateSlackSettingsMutation(graphene.Mutation):
    class Arguments:
        input = SlackSettingsInputType(required=True)

    status = graphene.Int()
    form_errors = graphene.String()
    slack_settings = graphene.Field(SlackSettingsType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return CreateSlackSettingsMutation(status=403,
                                               form_errors={'message': ['Unauthorized']})

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            return CreateSlackSettingsMutation(status=400,
                                               form_errors={'message': ['Invalid Slack Team Id']})

        slack_settings = SlackSettings.objects.create(**input)
        return CreateSlackSettingsMutation(slack_settings=slack_settings, status=201)


class Mutation(graphene.ObjectType):
    create_slack_user = CreateSlackUserMutation.Field()
    create_slack_team = CreateSlackTeamMutation.Field()
    create_slack_channel = CreateSlackChannelMutation.Field()
    create_slack_settings = CreateSlackSettingsMutation.Field()
