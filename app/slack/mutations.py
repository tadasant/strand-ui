import graphene

from app.groups.models import Group
from app.messages.models import Message, Reply
from app.messages.types import MessageType, ReplyType
from app.questions.models import Session
from app.questions.types import SessionType
from app.slack.models import SlackChannel, SlackEvent, SlackSettings, SlackTeam, SlackUser
from app.slack.types import (
    SessionAndSlackChannelInputType,
    SlackChannelType,
    SlackChannelInputType,
    SlackEventAndMessageInputType,
    SlackEventAndReplyInputType,
    SlackEventType,
    SlackSettingsType,
    SlackSettingsInputType,
    SlackTeamType,
    SlackTeamInputType,
    SlackUserType,
    SlackUserInputType
)
from app.users.models import User


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
        session.participants.add(author)

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
        message.session.participants.add(author)

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


class Mutation(graphene.ObjectType):
    create_slack_user = CreateSlackUserMutation.Field()
    create_slack_team = CreateSlackTeamMutation.Field()
    create_slack_channel = CreateSlackChannelMutation.Field()
    create_slack_settings = CreateSlackSettingsMutation.Field()

    create_slack_event_and_message = CreateSlackEventAndMessageMutation.Field()
    create_slack_event_and_reply = CreateSlackEventAndReplyMutation.Field()

    create_session_and_slack_channel = CreateSessionAndSlackChannelMutation.Field()
