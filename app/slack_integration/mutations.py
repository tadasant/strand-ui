from django.conf import settings
import graphene
import requests
from slackclient import SlackClient

from app.groups.models import Group
from app.groups.types import GroupType
from app.discussions.models import Message
from app.discussions.types import MessageType, ReplyType
from app.discussions.validators import MessageValidator, ReplyValidator
from app.questions.models import Question, Session
from app.questions.types import SessionType, QuestionType
from app.questions.validators import QuestionValidator, SessionValidator
from app.slack_integration.models import (
    SlackEvent,
    SlackTeamInstallation,
    SlackTeam,
    SlackUser
)
from app.slack_integration.types import (
    GroupFromSlackInputType,
    MessageFromSlackInputType,
    QuestionFromSlackInputType,
    ReplyFromSlackInputType,
    SessionFromSlackInputType,
    SlackChannelType,
    SlackChannelInputType,
    SlackEventType,
    SlackTeamType,
    SlackTeamInputType,
    SlackTeamInstallationHelpChannelAndActivateInputType,
    SlackTeamInstallationType,
    SlackTeamInstallationInputType,
    SlackUserType,
    SlackUserInputType,
    SolveQuestionFromSlackInputType,
    UserFromSlackInputType,
    UserAndMessageFromSlackInputType,
    UserAndQuestionFromSlackInputType,
    UserAndReplyFromSlackInputType
)
from app.slack_integration.validators import (
    SlackChannelValidator,
    SlackTeamValidator,
    SlackTeamInstallationValidator,
    SlackUserValidator
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

        slack_user_validator = SlackUserValidator(data=input)
        slack_user_validator.is_valid(raise_exception=True)
        slack_user = slack_user_validator.save()

        return CreateSlackUserMutation(slack_user=slack_user)


class CreateSlackChannelMutation(graphene.Mutation):
    class Arguments:
        input = SlackChannelInputType(required=True)

    slack_channel = graphene.Field(SlackChannelType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        slack_channel_validator = SlackChannelValidator(data=input)
        slack_channel_validator.is_valid(raise_exception=True)
        slack_channel = slack_channel_validator.save()

        return CreateSlackChannelMutation(slack_channel=slack_channel)


class CreateSlackTeamMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamInputType(required=True)

    slack_team = graphene.Field(SlackTeamType)

    def mutate(self, info, input):
        response = requests.get('https://slack.com/api/oauth.access',
                                params={'code': input.code, 'client_id': settings.SLACK_CLIENT_ID,
                                        'client_secret': settings.SLACK_CLIENT_SECRET})
        if not response.json().get('ok'):
            raise Exception(f'''Error accessing OAuth: {response.json()['error']}''')
        oauth_info = response.json()

        slack_client = SlackClient(oauth_info['access_token'])

        response = slack_client.api_call('team.info')
        if not response.get('ok'):
            raise Exception(f'''Error accessing team.info: {response.get('error')}''')
        team_info = response.get('team')

        response = slack_client.api_call('users.info', user=oauth_info['user_id'])
        if not response.get('ok'):
            raise Exception(f'''Error accessing users.info: {response.get('error')}''')
        user_info = response.get('user')

        group, _ = Group.objects.get_or_create(name=team_info['name'])
        slack_team = SlackTeam.objects.create(id=team_info['id'], name=team_info['name'], group=group)
        user, _ = User.objects.get_or_create(email=user_info['profile'].get('email'),
                                             defaults=dict(username=user_info['profile'].get('display_name') or
                                                                    user_info.get('name'),
                                                           first_name=user_info.get('first_name', ''),
                                                           last_name=user_info.get('last_name', ''),
                                                           avatar_url=user_info['profile'].get('image_72')))
        slack_user = SlackUser.objects.create(id=user_info['id'],
                                              name=user_info.get('name'),
                                              first_name=user_info.get('first_name', ''),
                                              last_name=user_info.get('last_name', ''),
                                              real_name=user_info.get('real_name'),
                                              display_name=user_info['profile'].get('display_name'),
                                              email=user_info['profile'].get('email'),
                                              avatar_72=user_info['profile'].get('image_72'),
                                              is_bot=user_info.get('is_bot'),
                                              is_admin=user_info.get('is_admin'),
                                              slack_team=slack_team,
                                              user=user)
        SlackTeamInstallation.objects.create(slack_team=slack_team,
                                             access_token=oauth_info['access_token'],
                                             scope=oauth_info['scope'],
                                             installer=slack_user,
                                             bot_user_id=oauth_info['bot']['bot_user_id'],
                                             bot_access_token=oauth_info['bot']['bot_access_token'])
        return CreateSlackTeamMutation(slack_team=slack_team)


class CreateSlackTeamInstallationMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamInstallationInputType(required=True)

    slack_team_installation = graphene.Field(SlackTeamInstallationType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        slack_team_installation_validator = SlackTeamInstallationValidator(data=input)
        slack_team_installation_validator.is_valid(raise_exception=True)
        slack_team_installation = slack_team_installation_validator.save()

        return CreateSlackTeamInstallationMutation(slack_team_installation=slack_team_installation)


class UpdateSlackTeamInstallationHelpChannelAndActivateMutation(graphene.Mutation):
    class Arguments:
        input = SlackTeamInstallationHelpChannelAndActivateInputType(required=True)

    slack_team_installation = graphene.Field(SlackTeamInstallationType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        slack_team_installation = SlackTeamInstallation.objects.get(slack_team__id=input.pop('slack_team_id'))
        slack_team_installation_validator = SlackTeamInstallationValidator(slack_team_installation,
                                                                           data=input,
                                                                           partial=True)
        slack_team_installation_validator.is_valid(raise_exception=True)
        slack_team_installation = slack_team_installation_validator.save()
        slack_team_installation.activate()

        return UpdateSlackTeamInstallationHelpChannelAndActivateMutation(
            slack_team_installation=slack_team_installation)


class CreateMessageFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = MessageFromSlackInputType(required=True)

    slack_event = graphene.Field(SlackEventType)
    message = graphene.Field(MessageType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        slack_event = SlackEvent.objects.create(ts=input['origin_slack_event_ts'])
        session = Session.objects.get(slackchannel__id=input['slack_channel_id'])
        author = User.objects.get(slack_users__id=input['slack_user_id'])

        message_validator = MessageValidator(data=dict(text=input['text'], time=input['time'], session_id=session.id,
                                                       author_id=author.id, origin_slack_event_id=slack_event.id))
        message_validator.is_valid(raise_exception=True)
        message = message_validator.save()

        session.participants.add(author)

        return CreateMessageFromSlackMutation(slack_event=slack_event, message=message)


class CreateUserAndMessageFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserAndMessageFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)
    message = graphene.Field(MessageType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

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
        session = Session.objects.get(slackchannel__id=input['slack_channel_id'])

        message_validator = MessageValidator(data=dict(text=input['text'], time=input['time'], session_id=session.id,
                                                       author_id=user.id, origin_slack_event_id=slack_event.id))
        message_validator.is_valid(raise_exception=True)
        message = message_validator.save()

        session.participants.add(user)

        return CreateUserAndMessageFromSlackMutation(user=user, slack_user=slack_user, message=message)


class CreateReplyFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = ReplyFromSlackInputType(required=True)

    slack_event = graphene.Field(SlackEventType)
    reply = graphene.Field(ReplyType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        slack_event = SlackEvent.objects.create(ts=input.pop('origin_slack_event_ts'))
        message = Message.objects.get(origin_slack_event__ts=input['message_origin_slack_event_ts'],
                                      session__slackchannel__id=input['slack_channel_id'])
        author = User.objects.get(slack_users__id=input['slack_user_id'])

        reply_validator = ReplyValidator(data=dict(text=input['text'], message_id=message.id, author_id=author.id,
                                                   origin_slack_event_id=slack_event.id, time=input['time']))
        reply_validator.is_valid(raise_exception=True)
        reply = reply_validator.save()

        message.session.participants.add(author)

        return CreateReplyFromSlackMutation(slack_event=slack_event, reply=reply)


class CreateUserAndReplyFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserAndReplyFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)
    reply = graphene.Field(ReplyType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

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
                                      session__slackchannel__id=input['slack_channel_id'])

        reply_validator = ReplyValidator(data=dict(text=input['text'], time=input['time'], author_id=user.id,
                                                   message_id=message.id, origin_slack_event_id=slack_event.id))
        reply_validator.is_valid(raise_exception=True)
        reply = reply_validator.save()

        message.session.participants.add(user)

        return CreateUserAndReplyFromSlackMutation(user=user, slack_user=slack_user, reply=reply)


class CreateSessionFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = SessionFromSlackInputType(required=True)

    session = graphene.Field(SessionType)
    slack_channel = graphene.Field(SlackChannelType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        session_validator = SessionValidator(data=input.pop('session', {}))
        session_validator.is_valid(raise_exception=True)
        session = session_validator.save()

        slack_channel_validator = SlackChannelValidator(data=dict(**input, session_id=session.id))
        slack_channel_validator.is_valid(raise_exception=True)
        slack_channel = slack_channel_validator.save()

        return CreateSessionFromSlackMutation(session=session, slack_channel=slack_channel)


class CreateUserFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        slack_user_validator = SlackUserValidator(data=input.pop('slack_user'), partial=True)
        slack_user_validator.is_valid(raise_exception=True)
        slack_user = SlackUser(**slack_user_validator.validated_data)

        try:
            user = User.objects.get(email=slack_user_validator.validated_data.get('email'))
            slack_user.user = user
            slack_user.save()
        except User.DoesNotExist:
            user = User.objects.create_user_from_slack_user(slack_user)

        return CreateUserFromSlackMutation(user=user, slack_user=slack_user)


class CreateGroupFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = GroupFromSlackInputType(required=True)

    group = graphene.Field(GroupType)
    slack_team = graphene.Field(SlackTeamType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        group, _ = Group.objects.get_or_create(name=input.get('group_name'))
        slack_team_validator = SlackTeamValidator(data=dict(id=input['slack_team_id'],
                                                            name=input['slack_team_name'],
                                                            group_id=group.id))
        slack_team_validator.is_valid(raise_exception=True)
        slack_team = slack_team_validator.save()

        return CreateGroupFromSlackMutation(group=group, slack_team=slack_team)


class CreateQuestionFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = QuestionFromSlackInputType(required=True)

    question = graphene.Field(QuestionType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        slack_user = SlackUser.objects.get(pk=input.pop('original_poster_slack_user_id'))
        tags = input.pop('tags', [])

        question_validator = QuestionValidator(data=dict(**input, original_poster_id=slack_user.user.id,
                                                         group_id=slack_user.slack_team.group.id))
        question_validator.is_valid(raise_exception=True)
        question = question_validator.save()

        question.add_or_create_tags(tags)

        return CreateQuestionFromSlackMutation(question=question)


class CreateUserAndQuestionFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = UserAndQuestionFromSlackInputType(required=True)

    user = graphene.Field(UserType)
    slack_user = graphene.Field(SlackUserType)
    question = graphene.Field(QuestionType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        slack_user_validator = SlackUserValidator(data=input.pop('slack_user'), partial=True)
        slack_user_validator.is_valid(raise_exception=True)
        slack_user = SlackUser(**slack_user_validator.validated_data)

        try:
            user = User.objects.get(email=slack_user_validator.validated_data.get('email'))
            slack_user.user = user
            slack_user.save()
        except User.DoesNotExist:
            user = User.objects.create_user_from_slack_user(slack_user)

        tags = input.pop('tags', [])

        question_validator = QuestionValidator(data=dict(**input, original_poster_id=slack_user.user.id,
                                                         group_id=slack_user.slack_team.group.id))
        question_validator.is_valid(raise_exception=True)
        question = question_validator.save()

        question.add_or_create_tags(tags)

        return CreateUserAndQuestionFromSlackMutation(user=user, slack_user=slack_user, question=question)


class SolveQuestionFromSlackMutation(graphene.Mutation):
    class Arguments:
        input = SolveQuestionFromSlackInputType(required=True)

    question = graphene.Field(QuestionType)
    session = graphene.Field(SessionType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        user = User.objects.get(slack_users__id=input['slack_user_id'])
        time_end = input.pop('time_end')

        question = Question.objects.get(session__slackchannel__id=input['slack_channel_id'])
        question_validator = QuestionValidator(question, data=dict(solver_id=user.id, is_solved=True), partial=True)
        question_validator.is_valid(raise_exception=True)
        question = question_validator.save()

        session = question.solve(time_end=time_end)

        return SolveQuestionFromSlackMutation(question=question, session=session)


class Mutation(graphene.ObjectType):
    create_slack_user = CreateSlackUserMutation.Field()
    create_slack_team = CreateSlackTeamMutation.Field()
    create_slack_channel = CreateSlackChannelMutation.Field()

    create_slack_team_installation = CreateSlackTeamInstallationMutation.Field()
    update_slack_team_installation_help_channel_and_activate = \
        UpdateSlackTeamInstallationHelpChannelAndActivateMutation.Field()

    create_message_from_slack = CreateMessageFromSlackMutation.Field()
    create_user_and_message_from_slack = CreateUserAndMessageFromSlackMutation.Field()

    create_reply_from_slack = CreateReplyFromSlackMutation.Field()
    create_user_and_reply_from_slack = CreateUserAndReplyFromSlackMutation.Field()

    create_question_from_slack = CreateQuestionFromSlackMutation.Field()
    create_user_and_question_from_slack = CreateUserAndQuestionFromSlackMutation.Field()

    create_session_from_slack = CreateSessionFromSlackMutation.Field()

    create_user_from_slack = CreateUserFromSlackMutation.Field()
    create_group_from_slack = CreateGroupFromSlackMutation.Field()

    solve_question_from_slack = SolveQuestionFromSlackMutation.Field()
