import pytest
from pytest_factoryboy.fixture import register
from rest_framework.test import APIClient

from tests.factories import (
    GroupFactory,
    GroupSettingFactory,
    MessageFactory,
    QuestionFactory,
    ReplyFactory,
    SessionFactory,
    SlackChannelFactory,
    SlackEventFactory,
    SlackTeamInstallationFactory,
    SlackTeamSettingFactory,
    SlackTeamFactory,
    SlackUserFactory,
    TagFactory,
    UserFactory
)

register(GroupFactory)
register(GroupSettingFactory)
register(MessageFactory)
register(QuestionFactory)
register(ReplyFactory)
register(SessionFactory)
register(SlackChannelFactory)
register(SlackEventFactory)
register(SlackTeamInstallationFactory)
register(SlackTeamSettingFactory)
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
