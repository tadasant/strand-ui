from datetime import datetime, timedelta

import pytest
import pytz
from django.conf import settings

from app.topics.models import Discussion
from tests.utils import wait_until


class TestMarkingDiscussionAsStale:
    @pytest.mark.django_db(transaction=True)
    def test_does_become_stale_with_no_messages(self, mark_stale_discussions_factory, discussion_factory,
                                                slack_app_request_factory):
        mark_stale_discussions_factory(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=58)
        discussion = discussion_factory(time_start=original_time)

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_stale, timeout=7)

        assert Discussion.objects.get(pk=discussion.id).is_stale
        assert len(slack_app_request_factory.calls) == 0

    @pytest.mark.django_db(transaction=True)
    def test_does_not_become_stale_with_non_bot_message(self, mark_stale_discussions_factory, auth_client,
                                                        discussion_factory, slack_channel_factory, message_factory,
                                                        user_factory, slack_user_factory, slack_event_factory,
                                                        slack_app_request_factory):
        mark_stale_discussions_factory(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=58)
        discussion = discussion_factory(time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)
        user = user_factory(is_bot=False)
        slack_user = slack_user_factory(user=user)
        slack_event = slack_event_factory.build(ts=(original_time + timedelta(minutes=2)).timestamp())
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_user.id}", originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_stale, timeout=5)

        assert not Discussion.objects.get(pk=discussion.id).is_stale
        assert len(slack_app_request_factory.calls) == 0

    @pytest.mark.django_db()
    def test_does_become_stale_with_bot_message(self, mark_stale_discussions_factory, auth_client, discussion_factory,
                                                slack_channel_factory, message_factory, user_factory,
                                                slack_user_factory, slack_event_factory, slack_app_request_factory):
        mark_stale_discussions_factory(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=57)
        discussion = discussion_factory(time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)
        user = user_factory(is_bot=True)
        slack_user = slack_user_factory(user=user)
        slack_event = slack_event_factory.build(ts=(original_time + timedelta(minutes=2)).timestamp())
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_user.id}", originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_stale, timeout=5)
        discussion = Discussion.objects.get(pk=discussion.id)

        assert discussion.is_stale
        assert len(slack_app_request_factory.calls) == 1
        assert slack_app_request_factory.calls[0].request.url == settings.SLACK_APP_STALE_DISCUSSION_ENDPOINT


class TestClosingPendingClosedDiscussion:
    @pytest.mark.django_db(transaction=True)
    def test_does_get_closed(self, auto_close_pending_closed_discussion_factory, auth_client, discussion_factory,
                             slack_channel_factory, message_factory, user_factory, slack_user_factory,
                             slack_event_factory, slack_app_request_factory):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        discussion = discussion_factory(time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)

        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)

        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=30)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), discussion=discussion)

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{non_bot_slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{ id }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        discussion.mark_as_stale()
        discussion.save()

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert not Discussion.objects.get(pk=discussion.id).is_closed

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_closed, timeout=5)
        discussion = Discussion.objects.get(pk=discussion.id)

        assert discussion.is_closed
        assert len(slack_app_request_factory.calls) == 1
        assert slack_app_request_factory.calls[0].request.url == settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT

    @pytest.mark.django_db
    def test_does_not_get_closed_with_non_bot_message(self, auto_close_pending_closed_discussion_factory,
                                                      auth_client, discussion_factory, slack_channel_factory,
                                                      message_factory, user_factory, slack_user_factory,
                                                      slack_event_factory, slack_app_request_factory):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        discussion = discussion_factory(time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)
        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)
        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=45)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), discussion=discussion)

        # Old message sent
        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{non_bot_slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{ id }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        # Discussion marked as stale
        discussion.mark_as_stale()
        discussion.save()

        # Discussion marked as pending closed
        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert not Discussion.objects.get(pk=discussion.id).is_closed

        # New message sent
        slack_event = slack_event_factory(ts=datetime.utcnow().timestamp())
        message = message_factory.build(discussion=discussion, author=non_bot_user)

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{non_bot_slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{ id }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_closed, timeout=5)

        assert not Discussion.objects.get(pk=discussion.id).is_closed
        assert len(slack_app_request_factory.calls) == 0

    @pytest.mark.django_db
    def test_does_get_closed_with_bot_message(self, auto_close_pending_closed_discussion_factory,
                                              auth_client, discussion_factory, slack_channel_factory,
                                              message_factory, user_factory, slack_user_factory,
                                              slack_event_factory, slack_app_request_factory):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        discussion = discussion_factory(time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)
        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)
        bot_user = user_factory(is_bot=True)
        bot_slack_user = slack_user_factory(user=bot_user)
        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=45)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), discussion=discussion)

        # Old message sent
        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{non_bot_slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{ id }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        # Discussion marked as stale
        discussion.mark_as_stale()
        discussion.save()

        # Discussion marked as pending closed
        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert not Discussion.objects.get(pk=discussion.id).is_closed
        assert len(slack_app_request_factory.calls) == 0

        # New message sent
        slack_event = slack_event_factory(ts=datetime.now(pytz.UTC).timestamp())
        message = message_factory.build(discussion=discussion, author=bot_user)

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{bot_slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{ id }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_closed, timeout=5)
        discussion = Discussion.objects.get(pk=discussion.id)

        assert discussion.is_closed
        assert len(slack_app_request_factory.calls) == 1
        assert slack_app_request_factory.calls[0].request.url == settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT

    @pytest.mark.django_db
    def test_does_get_closed_with_no_messages_ever(self, auto_close_pending_closed_discussion_factory,
                                                   auth_client, discussion_factory, slack_channel_factory,
                                                   slack_app_request_factory):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        discussion = discussion_factory(time_start=original_time)
        slack_channel = slack_channel_factory(discussion=discussion)

        discussion.mark_as_stale()
        discussion.save()

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_closed, timeout=5)
        discussion = Discussion.objects.get(pk=discussion.id)

        assert discussion.is_closed
        assert len(slack_app_request_factory.calls) == 1
        assert slack_app_request_factory.calls[0].request.url == settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT
