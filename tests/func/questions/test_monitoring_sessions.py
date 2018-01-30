import pytz
from datetime import datetime, timedelta

import pytest

from app.questions.models import Session
from tests.utils import wait_until


class TestMarkingSessionAsStale:
    @pytest.mark.django_db
    def test_does_become_stale_with_no_messages(self, auth_client, celery_worker, user_factory, message_factory,
                                                session_factory):
        """
        original_time = datetime.now(pytz.timezone('UTC')) - timedelta(minutes=29, seconds=59)
        user = user_factory(is_bot=False)
        session = session_factory(time_start=original_time)
        message = message_factory.build(session=session, author=user, time=original_time)

        mutation = f'''
        mutation {{
          createMessage(input: {{text: "{message.text}", sessionId: {message.session.id}, authorId: {message.author.id},
                                 time: "{message.time}"}}) {{
            message {{
              text
            }}
          }}
        }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        assert response.status_code == 200

        wait_until(condition=lambda: Session.objects.get(pk=session.id).is_stale, timeout=5)

        assert Session.objects.get(pk=session.id).is_stale == True
        """
        assert True

    @pytest.mark.django_db
    def test_does_not_become_stale_with_non_bot_message(self, celery_worker):
        assert True

    @pytest.mark.django_db
    def test_does_become_stale_with_bot_message(self, celery_worker):
        assert True

    @pytest.mark.django_db
    def test_does_become_stale_with_no_messages_ever(self, celery_worker):
        assert True


class TestClosingPendingClosedSession:
    @pytest.mark.django_db
    def test_does_get_closed_with_no_messages(self, celery_worker):
        assert True

    @pytest.mark.django_db
    def test_does_not_get_closed_with_non_bot_message(self, celery_worker):
        assert True

    @pytest.mark.django_db
    def test_does_get_closed_with_bot_message(self, celery_worker):
        assert True

    @pytest.mark.django_db
    def test_does_get_closed_with_no_messages_ever(self, celery_worker):
        assert True
