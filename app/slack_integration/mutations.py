from datetime import datetime

import graphene
import requests
from django.conf import settings
from slackclient import SlackClient

from app.api.authorization import check_authorization
from app.dialogues.models import Message
from app.dialogues.types import MessageType, ReplyType
from app.dialogues.validators import MessageValidator, ReplyValidator
from app.groups.models import Group
from app.slack_integration.models import (
    SlackAgent,
    SlackEvent,
    SlackTeam,
    SlackUser
)
from app.slack_integration.types import (
    MarkDiscussionAsPendingClosedFromSlackInputType,
    MessageFromSlackInputType,
    TopicFromSlackInputType,
    ReplyFromSlackInputType,
    DiscussionFromSlackInputType,
    SlackAgentTopicChannelAndActivateInputType,
    AttemptSlackInstallationInputType,
    SlackAgentType,
    SlackChannelType,
    SlackChannelInputType,
    SlackEventType,
    SlackUserType,
    SlackUserInputType,
    UserFromSlackInputType,
    UserAndMessageFromSlackInputType,
    UserAndTopicFromSlackInputType,
    UserAndReplyFromSlackInputType,
    CloseDiscussionFromSlackInputType, SlackTeamType)
from app.slack_integration.validators import (
    SlackChannelValidator,
    SlackUserValidator
)
from app.topics.models import Discussion
from app.topics.types import DiscussionType, TopicType
from app.topics.validators import TopicValidator, DiscussionValidator
from app.users.models import User
from app.users.types import UserType


class CreateSlackUserMutation(graphene.Mutation):
    class Arguments:
        input = SlackUserInputType(required=True)

    slack_user = graphene.Field(SlackUserType)

    @check_authorization
    def mutate(self, info, input):
        slack_user_validator = SlackUserValidator(data=input)
        slack_user_validator.is_valid(raise_exception=True)
        slack_user = slack_user_validator.save()

        return CreateSlackUserMutation(slack_user=slack_user)


class CreateSlackChannelMutation(graphene.Mutation):
    class Arguments:
        input = SlackChannelInputType(required=True)

    slack_channel = graphene.Field(SlackChannelType)

    @check_authorization
    def mutate(self, info, input):
        slack_channel_validator = SlackChannelValidator(data=input)
        slack_channel_validator.is_valid(raise_exception=True)
        slack_channel = slack_channel_validator.save()

        return CreateSlackChannelMutation(slack_channel=slack_channel)


class AttemptSlackInstallationMutation(graphene.Mutation):
    class Arguments:
        input = AttemptSlackInstallationInputType(required=True)

    slack_team = graphene.Field(SlackTeamType)

    def mutate(self, info, input):
        response = requests.get('https://slack.com/api/oauth.access',
                                params={'code': input.code, 'client_id': input.client_id,
                                        'client_secret': settings.SLACK_CLIENT_SECRET})
        if not response.json().get('ok'):
            raise Exception(f'''Error accessing OAuth: {response.json()['error']}''')
        oauth_info = response.json()

        slack_client = SlackClient(oauth_info['bot']['bot_access_token'])

        response = slack_client.api_call('team.info')
        if not response.get('ok'):
            raise Exception(f'''Error accessing team.info: {response.get('error')}''')
        team_info = response.get('team')

        response = slack_client.api_call('users.info', user=oauth_info['user_id'])
        if not response.get('ok'):
            raise Exception(f'''Error accessing users.info: {response.get('error')}''')
        user_info = response.get('user')

        group, _ = Group.objects.get_or_create(name=team_info['name'])
        slack_agent = SlackAgent.objects.create(group=group)
        slack_team = SlackTeam.objects.create(id=team_info['id'], name=team_info['name'], slack_agent=slack_agent)

        slack_user = SlackUser(id=user_info['id'], name=user_info.get('name'),
                               first_name=user_info.get('first_name', ''),
                               last_name=user_info.get('last_name', ''),
                               real_name=user_info.get('real_name'),
                               display_name=user_info['profile'].get('display_name'),
                               email=user_info['profile'].get('email'),
                               image_72=user_info['profile'].get('image_72'),
                               is_bot=user_info.get('is_bot'), is_admin=user_info.get('is_admin'),
                               slack_team=slack_team)

        try:
            user = User.objects.get(email=user_info['profile'].get('email'))
            slack_user.user = user
            slack_user.save()
        except User.DoesNotExist:
            User.objects.create_user_from_slack_user(slack_user)

        slack_agent.create_slack_application_installation_from_oauth(oauth_info)
        slack_agent.authenticate()
        slack_agent.save()

        return AttemptSlackInstallationMutation(slack_team=slack_team)


class UpdateSlackAgentTopicChannelAndActivateMutation(graphene.Mutation):
    class Arguments:
        input = SlackAgentTopicChannelAndActivateInputType(required=True)

    slack_agent = graphene.Field(SlackAgentType)

    @check_authorization
    def mutate(self, info, input):
        slack_agent = SlackAgent.objects.get(slack_team__id=input['slack_team_id'])
        slack_agent.topic_channel_id = input['topic_channel_id']
        slack_agent.activate()
        slack_agent.save()

        return UpdateSlackAgentTopicChannelAndActivateMutation(slack_agent=slack_agent)


class CreateMessageFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = MessageFromSlackInputType(required=True)

    slack_event = graphene.Field(SlackEventType)
    message = graphene.Field(MessageType)

    @check_authorization
    def mutate(self, info, input):
        slack_event = SlackEvent.objects.create(ts=input['origin_slack_event_ts'])
        discussion = Discussion.objects.get(slack_channel__id=input['slack_channel_id'])
        author = User.objects.get(slack_users__id=input['slack_user_id'])

        time = datetime.fromtimestamp(int(slack_event.ts.split('.')[0]))
        message_validator = MessageValidator(data=dict(text=input['text'], time=time, discussion_id=discussion.id,
                                                       author_id=author.id, origin_slack_event_id=slack_event.id))
        message_validator.is_valid(raise_exception=True)
        message = message_validator.save()

        discussion.participants.add(author)

        return CreateMessageFromSlackMutation(slack_event=slack_event, message=message)


class CreateUserAndMessageFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserAndMessageFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)
    message = graphene.Field(MessageType)

    @check_authorization
    def mutate(self, info, input):
        slack_user_validator = SlackUserValidator(data=input.pop('slack_user'), partial=True)
        slack_user_validator.is_valid(raise_exception=True)
        slack_user = SlackUser(**slack_user_validator.validated_data)

        try:
            user = User.objects.get(email=slack_user_validator.validated_data.get('email'))
            slack_user.user = user
            slack_user.save()
        except User.DoesNotExist:
            user = User.objects.create_user_from_slack_user(slack_user)

        slack_event = SlackEvent.objects.create(ts=input.pop('origin_slack_event_ts'))
        discussion = Discussion.objects.get(slack_channel__id=input['slack_channel_id'])

        time = datetime.fromtimestamp(int(slack_event.ts.split('.')[0]))
        message_validator = MessageValidator(data=dict(text=input['text'], time=time, discussion_id=discussion.id,
                                                       author_id=user.id, origin_slack_event_id=slack_event.id))
        message_validator.is_valid(raise_exception=True)
        message = message_validator.save()

        discussion.participants.add(user)

        return CreateUserAndMessageFromSlackMutation(user=user, slack_user=slack_user, message=message)


class CreateReplyFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = ReplyFromSlackInputType(required=True)

    slack_event = graphene.Field(SlackEventType)
    reply = graphene.Field(ReplyType)

    @check_authorization
    def mutate(self, info, input):
        slack_event = SlackEvent.objects.create(ts=input.pop('origin_slack_event_ts'))
        message = Message.objects.get(origin_slack_event__ts=input['message_origin_slack_event_ts'],
                                      discussion__slack_channel__id=input['slack_channel_id'])
        author = User.objects.get(slack_users__id=input['slack_user_id'])

        time = datetime.fromtimestamp(int(slack_event.ts.split('.')[0]))
        reply_validator = ReplyValidator(data=dict(text=input['text'], message_id=message.id, author_id=author.id,
                                                   origin_slack_event_id=slack_event.id, time=time))
        reply_validator.is_valid(raise_exception=True)
        reply = reply_validator.save()

        message.discussion.participants.add(author)

        return CreateReplyFromSlackMutation(slack_event=slack_event, reply=reply)


class CreateUserAndReplyFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserAndReplyFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)
    reply = graphene.Field(ReplyType)

    @check_authorization
    def mutate(self, info, input):
        slack_user_validator = SlackUserValidator(data=input.pop('slack_user'), partial=True)
        slack_user_validator.is_valid(raise_exception=True)
        slack_user = SlackUser(**slack_user_validator.validated_data)

        try:
            user = User.objects.get(email=slack_user_validator.validated_data.get('email'))
            slack_user.user = user
            slack_user.save()
        except User.DoesNotExist:
            user = User.objects.create_user_from_slack_user(slack_user)

        slack_event = SlackEvent.objects.create(ts=input.pop('origin_slack_event_ts'))
        message = Message.objects.get(origin_slack_event__ts=input['message_origin_slack_event_ts'],
                                      discussion__slack_channel__id=input['slack_channel_id'])

        time = datetime.fromtimestamp(int(slack_event.ts.split('.')[0]))
        reply_validator = ReplyValidator(data=dict(text=input['text'], time=time, author_id=user.id,
                                                   message_id=message.id, origin_slack_event_id=slack_event.id))
        reply_validator.is_valid(raise_exception=True)
        reply = reply_validator.save()

        message.discussion.participants.add(user)

        return CreateUserAndReplyFromSlackMutation(user=user, slack_user=slack_user, reply=reply)


class CreateDiscussionFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = DiscussionFromSlackInputType(required=True)

    discussion = graphene.Field(DiscussionType)
    slack_channel = graphene.Field(SlackChannelType)

    @check_authorization
    def mutate(self, info, input):
        discussion_validator = DiscussionValidator(data=input.pop('discussion', {}))
        discussion_validator.is_valid(raise_exception=True)
        discussion = discussion_validator.save()

        slack_channel_validator = SlackChannelValidator(data=dict(**input, discussion_id=discussion.id))
        slack_channel_validator.is_valid(raise_exception=True)
        slack_channel = slack_channel_validator.save()

        return CreateDiscussionFromSlackMutation(discussion=discussion, slack_channel=slack_channel)


class CreateUserFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)

    @check_authorization
    def mutate(self, info, input):
        slack_user_validator = SlackUserValidator(data=input, partial=True)
        slack_user_validator.is_valid(raise_exception=True)
        slack_user = SlackUser(**slack_user_validator.validated_data)

        try:
            user = User.objects.get(email=slack_user_validator.validated_data.get('email'))
            slack_user.user = user
            slack_user.save()
        except User.DoesNotExist:
            user = User.objects.create_user_from_slack_user(slack_user)

        return CreateUserFromSlackMutation(user=user, slack_user=slack_user)


class CreateTopicFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = TopicFromSlackInputType(required=True)

    topic = graphene.Field(TopicType)

    @check_authorization
    def mutate(self, info, input):
        slack_user = SlackUser.objects.get(pk=input.pop('original_poster_slack_user_id'))
        tags = input.pop('tags', [])

        topic_validator = TopicValidator(data=dict(**input, original_poster_id=slack_user.user.id,
                                                   group_id=slack_user.slack_team.slack_agent.group.id))
        topic_validator.is_valid(raise_exception=True)
        topic = topic_validator.save()

        topic.add_or_create_tags(tags)

        return CreateTopicFromSlackMutation(topic=topic)


class CreateUserAndTopicFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserAndTopicFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)
    topic = graphene.Field(TopicType)

    @check_authorization
    def mutate(self, info, input):
        slack_user_validator = SlackUserValidator(data=input.pop('original_poster_slack_user'), partial=True)
        slack_user_validator.is_valid(raise_exception=True)
        slack_user = SlackUser(**slack_user_validator.validated_data)

        try:
            user = User.objects.get(email=slack_user_validator.validated_data.get('email'))
            slack_user.user = user
            slack_user.save()
        except User.DoesNotExist:
            user = User.objects.create_user_from_slack_user(slack_user)

        tags = input.pop('tags', [])

        topic_validator = TopicValidator(data=dict(**input, original_poster_id=slack_user.user.id,
                                                   group_id=slack_user.slack_team.slack_agent.group.id))
        topic_validator.is_valid(raise_exception=True)
        topic = topic_validator.save()

        topic.add_or_create_tags(tags)

        return CreateUserAndTopicFromSlackMutation(user=user, slack_user=slack_user, topic=topic)


class MarkDiscussionAsPendingClosedFromSlack(graphene.Mutation):
    class Arguments:
        input = MarkDiscussionAsPendingClosedFromSlackInputType(required=True)

    discussion = graphene.Field(DiscussionType)

    @check_authorization
    def mutate(self, info, input):
        discussion = Discussion.objects.get(slack_channel__id=input['slack_channel_id'])
        discussion.standby_to_auto_close()

        return MarkDiscussionAsPendingClosedFromSlack(discussion=discussion)


class CloseDiscussionFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = CloseDiscussionFromSlackInputType(required=True)

    discussion = graphene.Field(DiscussionType)

    @check_authorization
    def mutate(self, info, input):
        discussion = Discussion.objects.get(slack_channel__id=input['slack_channel_id'])
        slack_user = SlackUser.objects.get(id=input['slack_user_id'])

        if not slack_user.can_close_discussion(discussion):
            raise Exception('Slack user does not have permission to close discussion')

        discussion.mark_as_closed()
        discussion.save()
        return CloseDiscussionFromSlackMutation(discussion=discussion)


class Mutation(graphene.ObjectType):
    attempt_slack_installation = AttemptSlackInstallationMutation.Field()

    create_slack_user = CreateSlackUserMutation.Field()
    create_slack_channel = CreateSlackChannelMutation.Field()

    update_slack_agent_topic_channel_and_activate = UpdateSlackAgentTopicChannelAndActivateMutation.Field()

    create_message_from_slack = CreateMessageFromSlackMutation.Field()
    create_user_and_message_from_slack = CreateUserAndMessageFromSlackMutation.Field()

    create_reply_from_slack = CreateReplyFromSlackMutation.Field()
    create_user_and_reply_from_slack = CreateUserAndReplyFromSlackMutation.Field()

    create_topic_from_slack = CreateTopicFromSlackMutation.Field()
    create_user_and_topic_from_slack = CreateUserAndTopicFromSlackMutation.Field()

    create_discussion_from_slack = CreateDiscussionFromSlackMutation.Field()
    mark_discussion_as_pending_closed_from_slack = MarkDiscussionAsPendingClosedFromSlack.Field()
    create_user_from_slack = CreateUserFromSlackMutation.Field()
    close_discussion_from_slack = CloseDiscussionFromSlackMutation.Field()
