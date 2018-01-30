import os
import signal
import subprocess
import time

import pytest
import responses
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from pytest_factoryboy.fixture import register
from rest_framework.test import APIClient
from slackclient import SlackClient

from tests.factories import (
    GroupFactory,
    MessageFactory,
    QuestionFactory,
    ReplyFactory,
    SessionFactory,
    SlackAgentFactory,
    SlackChannelFactory,
    SlackEventFactory,
    SlackApplicationInstallationFactory,
    SlackTeamFactory,
    SlackUserFactory,
    TagFactory,
    UserFactory
)
from tests.resources.TestSlackClient import TestSlackClient

register(GroupFactory)
register(MessageFactory)
register(QuestionFactory)
register(ReplyFactory)
register(SessionFactory)
register(SlackAgentFactory)
register(SlackChannelFactory)
register(SlackEventFactory)
register(SlackApplicationInstallationFactory)
register(SlackTeamFactory)
register(SlackUserFactory)
register(TagFactory)
register(UserFactory)


@pytest.fixture()
def auth_client(user_factory):
    """Pytest fixture for authenticated API client

    Most of our mutations require authentication. Rather than authenticate
    with a mock user each time, this fixture allows us to use an already
    authenticated api client.
    """
    user = user_factory()
    client = APIClient()
    client.force_login(user=user)
    return client


@pytest.fixture()
def slack_oauth_request(request):
    """Pytest fixture for calls from requests to Slack

    Uses the responses library that was built at Dropbox to mock out
    requests. If we move to more calls via request, I recommend
    creating a test resource that handles each url we may want to access
    and we can parametrize controlling the responses similar to below.
    Alternative is to have a bunch of request mock fixtures on a per-
    resource basis.

    See: http://cra.mr/2014/05/20/mocking-requests-with-responses.
    """
    request_mock = responses.RequestsMock(False)
    request_mock.start()

    if request.param == 'valid_token':
        response = {'ok': True, 'access_token': '',
                    'scope': '',
                    'team_id': 'T8TQP6ABE',
                    'user_id': 'U8USTVANB',
                    'bot': {'bot_user_id': '',
                            'bot_access_token': ''}}
    else:
        response = {'ok': False, 'error': 'invalid_code'}

    request_mock.add(responses.GET, 'https://slack.com/api/oauth.access', json=response)

    yield request_mock

    request_mock.stop()
    request_mock.reset()


@pytest.fixture()
def slack_client_factory(mocker):
    """Pytest fixture to patch api_call using test resource

    Created a test slack client class that implements the init
    and api_call functions. Patching the api_call so that we can
    test successful responses. Future testing can take it one
    step further by wrapping the client in a fixture that controls
    the scope of the token.
    """
    mocker.patch.object(SlackClient, 'api_call', new=TestSlackClient.api_call)


@pytest.fixture()
def periodic_tasks():
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name='Mark stale sessions',
        task='app.questions.tasks.mark_stale_sessions'
    )
