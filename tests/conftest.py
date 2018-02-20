import pytest
import responses
from django.conf import settings
from pytest_factoryboy.fixture import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from slackclient import SlackClient

from app.topics.tasks import auto_close_pending_closed_discussion
from tests.factories import (
    GroupFactory,
    MessageFactory,
    TopicFactory,
    ReplyFactory,
    DiscussionFactory,
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
from tests.resources.test_celery_tasks import auto_close_pending_closed_discussion_task, mark_stale_discussions_task

register(GroupFactory)
register(MessageFactory)
register(TopicFactory)
register(ReplyFactory)
register(DiscussionFactory)
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
    token = Token.objects.get(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client


@pytest.fixture()
def slack_app_request_factory():
    """Pytest fixture for calls from requests to Slack App

    Uses the responses library that was built at Dropbox to mock
    out requests. We use this to ensure the requests was called.
    """
    request_mock = responses.RequestsMock(False)
    request_mock.start()

    request_mock.add(responses.POST, settings.SLACK_APP_SLACK_AGENT_ENDPOINT, status=200)
    request_mock.add(responses.PUT, settings.SLACK_APP_SLACK_AGENT_ENDPOINT, status=200)
    request_mock.add(responses.POST, settings.SLACK_APP_STALE_DISCUSSION_ENDPOINT, status=200)
    request_mock.add(responses.POST, settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT, status=200)

    yield request_mock

    request_mock.stop()
    request_mock.reset()


@pytest.fixture()
def slack_oauth_request(slack_app_request_factory, request):
    """Pytest fixture for calls from requests to Slack

    Uses the responses library that was built at Dropbox to mock out
    requests. If we move to more calls via request, I recommend
    creating a test resource that handles each url we may want to access
    and we can parametrize controlling the responses similar to below.
    Alternative is to have a bunch of request mock fixtures on a per-
    resource basis.

    See: http://cra.mr/2014/05/20/mocking-requests-with-responses.
    """
    if request.param == 'valid_token':
        response = {'ok': True, 'access_token': '',
                    'scope': '',
                    'team_id': 'T8TQP6ABE',
                    'user_id': 'U8USTVANB',
                    'bot': {'bot_user_id': '',
                            'bot_access_token': ''}}
    else:
        response = {'ok': False, 'error': 'invalid_code'}

    slack_app_request_factory.add(responses.GET, 'https://slack.com/api/oauth.access', json=response)
    slack_app_request_factory.add(responses.POST, settings.SLACK_APP_SLACK_AGENT_ENDPOINT, status=200)
    slack_app_request_factory.add(responses.PUT, settings.SLACK_APP_SLACK_AGENT_ENDPOINT, status=200)
    slack_app_request_factory.add(responses.POST, settings.SLACK_APP_STALE_DISCUSSION_ENDPOINT, status=200)
    slack_app_request_factory.add(responses.POST, settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT, status=200)

    yield slack_app_request_factory


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
def auto_close_pending_closed_discussion_factory(mocker, transactional_db):
    """Pytest fixture to patch async_delay using test resource

    Created a test resource for the auto_close_pending_closed_discussion
    task that executes after the intended delay without the need of
    a Celery worker.
    """
    mocker.patch.object(auto_close_pending_closed_discussion, 'apply_async',
                        new=auto_close_pending_closed_discussion_task)


@pytest.fixture()
def mark_stale_discussions_factory(transactional_db):
    """Pytest fixture to monitor for stale discussions.

    This is in lieu of creating mock resources to mimick a
    Celery Beat and Celery worker. This does a timed loop
    10 times and executes the mark_stale_discussion task.
    """
    return mark_stale_discussions_task
