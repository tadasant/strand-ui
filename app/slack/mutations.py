import graphene

from app.groups.models import Group
from app.groups.types import GroupType
from app.messages.models import Message, Reply
from app.messages.types import MessageType, ReplyType
from app.questions.models import Session
from app.questions.types import SessionType
from app.slack.models import (
    SlackChannel,
    SlackEvent,
    SlackTeamSetting,
    SlackTeamInstallation,
    SlackTeam,
    SlackUser
)
from app.slack.types import (
    GroupAndSlackTeamInputType,
    SessionAndSlackChannelInputType,
    SlackChannelType,
    SlackChannelInputType,
    SlackEventAndMessageInputType,
    SlackEventAndReplyInputType,
    SlackEventType,
    SlackTeamSettingType,
    SlackTeamSettingInputType,
    SlackTeamType,
    SlackTeamInputType,
    SlackTeamInstallationType,
    SlackTeamInstallationInputType,
    SlackUserType,
    SlackUserInputType,
    UserAndSlackUserInputType
)
from app.users.models import User
from app.users.types import UserType


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


class CreateSlackTeamSettingMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamSettingInputType(required=True)

    slack_team_setting = graphene.Field(SlackTeamSettingType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        slack_team_setting = SlackTeamSetting.objects.create(**input)

        return CreateSlackTeamSettingMutation(slack_team_setting=slack_team_setting)


class CreateSlackTeamInstallationMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamInstallationInputType(required=True)

    slack_team_installation = graphene.Field(SlackTeamInstallationType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            raise Exception('Invalid Slack Team Id')

        slack_team_installation = SlackTeamInstallation.objects.create(**input)

        return CreateSlackTeamInstallationMutation(slack_team_installation=slack_team_installation)


class CreateSlackEventAndMessageMutation(graphene.Mutation):
    class Arguments:
        input = SlackEventAndMessageInputType(required=True)

    slack_event = graphene.Field(SlackEventType)
    message = graphene.Field(MessageType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackUser.objects.filter(pk=input['slack_user_id']).exists():
            raise Exception('Invalid Slack User Id')

        if not SlackChannel.objects.filter(pk=input['slack_channel_id']).exists():
            raise Exception('Invalid Slack Channel Id')

        ts = input.pop('slack_event_ts')
        slack_event = SlackEvent.objects.create(ts=ts)

        session = Session.objects.get(slackchannel__id=input['slack_channel_id'])
        author = User.objects.get(slackuser__id=input['slack_user_id'])
        message = Message.objects.create(text=input['text'], session=session, author=author,
                                         time=input['time'], slack_event=slack_event)

        return CreateSlackEventAndMessageMutation(slack_event=slack_event, message=message)


class CreateSlackEventAndReplyMutation(graphene.Mutation):
    class Arguments:
        input = SlackEventAndReplyInputType(required=True)

    slack_event = graphene.Field(SlackEventType)
    reply = graphene.Field(ReplyType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackUser.objects.filter(pk=input['slack_user_id']).exists():
            raise Exception('Invalid Slack User Id')

        if not SlackChannel.objects.filter(pk=input['slack_channel_id']).exists():
            raise Exception('Invalid Slack Channel Id')

        if not Message.objects.filter(slack_event__ts=input['message_slack_event_ts'],
                                      session__slackchannel__id=input['slack_channel_id']).exists():
            raise Exception('Invalid Message Slack Event Ts')

        ts = input.pop('slack_event_ts')
        slack_event = SlackEvent.objects.create(ts=ts)
        message = Message.objects.get(slack_event__ts=input['message_slack_event_ts'],
                                      session__slackchannel__id=input['slack_channel_id'])
        author = User.objects.get(slackuser__id=input['slack_user_id'])
        reply = Reply.objects.create(text=input['text'], message=message, author=author,
                                     time=input['time'], slack_event=slack_event)

        return CreateSlackEventAndReplyMutation(slack_event=slack_event, reply=reply)


class CreateSessionAndSlackChannelMutation(graphene.Mutation):
    class Arguments:
        input = SessionAndSlackChannelInputType(required=True)

    session = graphene.Field(SessionType)
    slack_channel = graphene.Field(SlackChannelType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        session_args = input.pop('session', {})
        session = Session.objects.create(**session_args)
        channel = SlackChannel.objects.create(**input, session_id=session.id)

        return CreateSessionAndSlackChannelMutation(session=session, slack_channel=channel)


class GetOrCreateUserAndCreateSlackUserMutation(graphene.Mutation):
    class Arguments:
        input = UserAndSlackUserInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not SlackTeam.objects.filter(pk=input['slack_team_id']).exists():
            raise Exception('Invalid Slack Team Id')

        if SlackUser.objects.filter(id=input['id'], slack_team__id=input['slack_team_id']).exists():
            raise Exception(f'''Slack User with id {input['id']} already exists''')

        slack_team = SlackTeam.objects.get(pk=input['slack_team_id'])
        user, created = User.objects.get_or_create(email=input['email'],
                                                   defaults=dict(username=input['display_name'],
                                                                 first_name=input.get('first_name'),
                                                                 last_name=input.get('last_name'),
                                                                 avatar_url=input.get('avatar_72')))
        slack_team.group.members.add(user)
        slack_user = SlackUser.objects.create(**input, user=user)

        return GetOrCreateUserAndCreateSlackUserMutation(user=user, slack_user=slack_user)


class GetOrCreateGroupAndCreateSlackTeamMutation(graphene.Mutation):
    class Arguments:
        input = GroupAndSlackTeamInputType(required=True)

    group = graphene.Field(GroupType)
    slack_team = graphene.Field(SlackTeamType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if SlackTeam.objects.filter(pk=input['slack_team_id']).exists():
            raise Exception(f'''Slack Team with id {input['slack_team_id']} already exists''')

        group_name = input.pop('group_name')
        group, created = Group.objects.get_or_create(name=group_name)
        slack_team = SlackTeam.objects.create(id=input['slack_team_id'], name=input['slack_team_name'], group=group)

        return GetOrCreateGroupAndCreateSlackTeamMutation(group=group, slack_team=slack_team)


class Mutation(graphene.ObjectType):
    create_slack_user = CreateSlackUserMutation.Field()
    create_slack_team = CreateSlackTeamMutation.Field()
    create_slack_channel = CreateSlackChannelMutation.Field()
    create_slack_team_setting = CreateSlackTeamSettingMutation.Field()
    create_slack_team_installation = CreateSlackTeamInstallationMutation.Field()

    create_slack_event_and_message = CreateSlackEventAndMessageMutation.Field()
    create_slack_event_and_reply = CreateSlackEventAndReplyMutation.Field()

    create_session_and_slack_channel = CreateSessionAndSlackChannelMutation.Field()

    get_or_create_user_and_create_slack_user = GetOrCreateUserAndCreateSlackUserMutation.Field()
    get_or_create_group_and_create_slack_team = GetOrCreateGroupAndCreateSlackTeamMutation.Field()
