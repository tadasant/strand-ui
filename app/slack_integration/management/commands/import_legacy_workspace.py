import re
from datetime import datetime

from django.core.management.base import BaseCommand
from slackclient import SlackClient

from app.discussions.models import Message, Reply
from app.groups.models import Group
from app.topics.models import Topic, Session, Tag
from app.slack_integration.models import SlackTeam, SlackChannel, SlackEvent, SlackUser
from app.users.models import User


class Command(BaseCommand):
    help = 'Imports Slack team for development'

    def add_arguments(self, parser):
        parser.add_argument('slack_api_token', type=str)
        parser.add_argument('bot_id', type=str)

    def handle(self, *args, **options):
        client = SlackClient(options['slack_api_token'])
        group, slack_team = create_group_and_slack_team(client)

        create_users_and_slack_users(client, group, slack_team)

        create_topics_and_sessions(client, slack_team, options['bot_id'])


def create_group_and_slack_team(client):
    response = client.api_call('team.info')
    team_info = response.get('team')
    group = Group.objects.create(name=team_info.get('name'))
    slack_team = SlackTeam.objects.create(id=team_info.get('id'), name=team_info.get('name'), group=group)
    return group, slack_team


def create_users_and_slack_users(client, group, slack_team):
    response = client.api_call('users.list')
    users_info = response.get('members')
    for user_info in users_info:
        user, created = User.objects.get_or_create(email=user_info['profile'].get('email'),
                                                   defaults=dict(username=(user_info['profile'].get('display_name') or
                                                                           user_info.get('name')),
                                                                 first_name=user_info['profile'].get('first_name'),
                                                                 last_name=user_info['profile'].get('last_name'),
                                                                 avatar_url=user_info['profile'].get('image_72')))
        SlackUser.objects.create(id=user_info.get('id'),
                                 name=user_info.get('name'),
                                 first_name=user_info['profile'].get('first_name'),
                                 last_name=user_info['profile'].get('last_name'),
                                 real_name=user_info.get('real_name', ''),
                                 display_name=user_info['profile'].get('display_name'),
                                 email=user_info['profile'].get('email'),
                                 avatar_72=user_info['profile'].get('image_72'),
                                 is_bot=user_info.get('is_bot'),
                                 is_admin=user_info.get('is_admin', False),
                                 slack_team=slack_team,
                                 user=user)
        group.members.add(user)


def get_topic_info(messages, bot_id):
    for message in reversed(messages):
        if (all([x in message.get('text').lower() for x in ('title', 'description', 'tags')]) and message.get(
                'user') == bot_id):
            try:
                topic_text = message.get('text')
                title = re.search(r'[T|t]itle(?:.*?) (.*?)[\n]', topic_text, re.DOTALL).group(1)
                tags = re.search(r'[T|t]ags(?:.*?) (.*?)[\n]', topic_text, re.DOTALL).group(1).split(',')
                tags = [tag.strip().lower().replace(' ', '-') for tag in tags]
                description = re.search(r'[D|d]escription(?:.*?) (.*?)$', topic_text, re.DOTALL).group(1).strip('\n')
                return {'title': title, 'tags': tags, 'description': description}
            except AttributeError:
                continue
    return {}


def is_valid_channel_history(messages):
    for message in messages:
        if all([x in message.get('text').lower() for x in ('title', 'description', 'tags')]):
            return True
    return False


def get_messages(events):
    messages = []
    for event in events:
        if (event.get('subtype') == 'file_share' or not event.get('subtype')) and not event.get('parent_user_id'):
            time = datetime.fromtimestamp(int(event.get('ts').split('.')[0]))
            message = {'slack_event_ts': event.get('ts'), 'text': event.get('text'), 'time': time,
                       'slack_user_id': event.get('user')}
            messages.append(message)
    return messages


def get_replies(events):
    replies = []
    for event in events:
        if (event.get('subtype') == 'file_share' or not event.get('subtype')) and event.get('parent_user_id'):
            time = datetime.fromtimestamp(int(event.get('ts').split('.')[0]))
            reply = {'slack_event_ts': event.get('ts'), 'text': event.get('text'), 'time': time,
                     'slack_user_id': event.get('user'), 'message_slack_event_ts': event.get('thread_ts')}
            replies.append(reply)
    return replies


def create_topics_and_sessions(client, slack_team, bot_id):
    response = client.api_call('channels.list')
    channels_info = response.get('channels')
    filtered_channels_info = filter(lambda x: 'session-' in x['name'], channels_info)
    for channel_info in filtered_channels_info:
        channel_history = client.api_call('channels.history', channel=channel_info['id'], count=500)

        if is_valid_channel_history(channel_history['messages']):
            channel = client.api_call('channels.info', channel=channel_info['id'])['channel']
            temp_original_poster = User.objects.get(slackuser__id=bot_id)
            topic_info = get_topic_info(channel_history['messages'], bot_id)

            if not topic_info.get('title'):
                continue

            messages = get_messages(channel_history['messages'])
            replies = get_replies(channel_history['messages'])
            participants = list(set([message['slack_user_id'] for message in messages] +
                                    [reply['slack_user_id'] for reply in replies]))

            topic = Topic.objects.create(title=topic_info['title'], description=topic_info['description'],
                                               original_poster=temp_original_poster, group=slack_team.group)

            for tag_name in topic_info.get('tags', []):
                tag, created = Tag.objects.get_or_create(name=tag_name)
                topic.tags.add(tag)

            session = Session.objects.create(topic=topic, time_start=messages[-1]['time'],
                                             time_end=messages[0]['time'])
            session.participants.set(User.objects.filter(slackuser__id__in=participants))

            slack_channel = SlackChannel.objects.create(id=channel['id'], name=channel['name'],
                                                        slack_team=slack_team, session=session)

            for message in messages:
                author = User.objects.get(slackuser__id=message['slack_user_id'])
                slack_event = SlackEvent.objects.create(ts=message['slack_event_ts'])
                Message.objects.create(text=message['text'], time=message['time'], origin_slack_event=slack_event,
                                       author=author, session=session)

            for reply in replies:
                author = User.objects.get(slackuser__id=reply['slack_user_id'])
                slack_event = SlackEvent.objects.create(ts=reply['slack_event_ts'])
                message = Message.objects.get(origin_slack_event__ts=reply['message_slack_event_ts'],
                                              session__slackchannel__id=slack_channel.id)
                Reply.objects.create(text=reply['text'], time=reply['time'], origin_slack_event=slack_event,
                                     author=author, message=message)
