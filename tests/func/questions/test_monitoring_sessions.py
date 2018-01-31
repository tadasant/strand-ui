import pytz
from datetime import datetime, timedelta

import pytest

from app.questions.models import Session
from tests.utils import wait_until


class TestMarkingSessionAsStale:
    @pytest.mark.django_db(transaction=True)
    def test_does_become_stale_with_no_messages(self, mark_stale_sessions_factory, session_factory):
        mark_stale_sessions_factory(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=58)
        session = session_factory(time_start=original_time)

        wait_until(condition=lambda: Session.objects.get(pk=session.id).is_stale, timeout=7)

        assert Session.objects.get(pk=session.id).is_stale

    @pytest.mark.django_db(transaction=True)
    def test_does_not_become_stale_with_non_bot_message(self, mark_stale_sessions_factory, auth_client, session_factory,
                                                        slack_channel_factory, message_factory, user_factory,
                                                        slack_user_factory, slack_event_factory):
        mark_stale_sessions_factory(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=58)
        session = session_factory(time_start=original_time)
        slack_channel = slack_channel_factory(session=session)
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

        wait_until(condition=lambda: Session.objects.get(pk=session.id).is_stale, timeout=5)

        assert not Session.objects.get(pk=session.id).is_stale

    @pytest.mark.django_db()
    def test_does_become_stale_with_bot_message(self, mark_stale_sessions_factory, auth_client, session_factory,
                                                slack_channel_factory, message_factory, user_factory,
                                                slack_user_factory, slack_event_factory):
        mark_stale_sessions_factory(num_periods=3, period_length=1.5)

        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=29, seconds=57)
        session = session_factory(time_start=original_time)
        slack_channel = slack_channel_factory(session=session)
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

        wait_until(condition=lambda: Session.objects.get(pk=session.id).is_stale, timeout=5)

        assert Session.objects.get(pk=session.id).is_stale


class TestClosingPendingClosedSession:
    @pytest.mark.django_db(transaction=True)
    def test_does_get_closed(self, auto_close_pending_closed_session_factory, auth_client, session_factory,
                             slack_channel_factory, message_factory, user_factory, slack_user_factory,
                             slack_event_factory):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        session = session_factory(time_start=original_time)
        slack_channel = slack_channel_factory(session=session)

        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)

        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=30)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), session=session)

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

        session.mark_as_stale()
        session.save()

        mutation = f'''
          mutation {{
            markSessionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              session {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert not Session.objects.get(pk=session.id).is_closed

        wait_until(condition=lambda: Session.objects.get(pk=session.id).is_closed, timeout=5)

        assert Session.objects.get(pk=session.id).is_closed

    @pytest.mark.django_db
    def test_does_not_get_closed_with_non_bot_message(self, auto_close_pending_closed_session_factory,
                                                      auth_client, session_factory, slack_channel_factory,
                                                      message_factory, user_factory, slack_user_factory,
                                                      slack_event_factory):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        session = session_factory(time_start=original_time)
        slack_channel = slack_channel_factory(session=session)
        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)
        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=45)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), session=session)

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

        # Session marked as stale
        session.mark_as_stale()
        session.save()

        # Session marked as pending closed
        mutation = f'''
          mutation {{
            markSessionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              session {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert not Session.objects.get(pk=session.id).is_closed

        # New message sent
        slack_event = slack_event_factory(ts=datetime.utcnow().timestamp())
        message = message_factory.build(session=session, author=non_bot_user)

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

        wait_until(condition=lambda: Session.objects.get(pk=session.id).is_closed, timeout=5)

        assert not Session.objects.get(pk=session.id).is_closed

    @pytest.mark.django_db
    def test_does_get_closed_with_bot_message(self, auto_close_pending_closed_session_factory,
                                              auth_client, session_factory, slack_channel_factory,
                                              message_factory, user_factory, slack_user_factory,
                                              slack_event_factory):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        session = session_factory(time_start=original_time)
        slack_channel = slack_channel_factory(session=session)
        non_bot_user = user_factory(is_bot=False)
        non_bot_slack_user = slack_user_factory(user=non_bot_user)
        bot_user = user_factory(is_bot=True)
        bot_slack_user = slack_user_factory(user=bot_user)
        slack_event = slack_event_factory(ts=(original_time + timedelta(seconds=45)).timestamp())
        message = message_factory.build(time=original_time + timedelta(seconds=30), session=session)

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

        # Session marked as stale
        session.mark_as_stale()
        session.save()

        # Session marked as pending closed
        mutation = f'''
          mutation {{
            markSessionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              session {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert not Session.objects.get(pk=session.id).is_closed

        # New message sent
        slack_event = slack_event_factory(ts=datetime.now(pytz.UTC).timestamp())
        message = message_factory.build(session=session, author=bot_user)

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

        wait_until(condition=lambda: Session.objects.get(pk=session.id).is_closed, timeout=5)

        assert Session.objects.get(pk=session.id).is_closed

    @pytest.mark.django_db
    def test_does_get_closed_with_no_messages_ever(self, auto_close_pending_closed_session_factory,
                                                   auth_client, session_factory, slack_channel_factory):
        original_time = datetime.now(tz=pytz.UTC) - timedelta(minutes=31)
        session = session_factory(time_start=original_time)
        slack_channel = slack_channel_factory(session=session)

        session.mark_as_stale()
        session.save()

        mutation = f'''
          mutation {{
            markSessionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              session {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        wait_until(condition=lambda: Session.objects.get(pk=session.id).is_closed, timeout=5)
        session = Session.objects.get(pk=session.id)

        assert session.is_closed
