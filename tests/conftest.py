import pytest
from pytest_factoryboy.fixture import register
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


from tests.factories import (
    GroupFactory,
    GroupSettingsFactory,
    MessageFactory,
    QuestionFactory,
    ReplyFactory,
    SessionFactory,
    SlackChannelFactory,
    SlackEventFactory,
    SlackSettingsFactory,
    SlackTeamFactory,
    SlackUserFactory,
    TagFactory,
    UserFactory
)

register(GroupFactory)
register(GroupSettingsFactory)
register(MessageFactory)
register(QuestionFactory)
register(ReplyFactory)
register(SessionFactory)
register(SlackChannelFactory)
register(SlackEventFactory)
register(SlackSettingsFactory)
register(SlackTeamFactory)
register(SlackUserFactory)
register(TagFactory)
register(UserFactory)


@pytest.fixture()
def auth_client(user_factory):
    """Pytest fixure for authenticated API client"""
    user = user_factory()
    client = APIClient()
    client.force_login(user=user)
    return client
