from pytest_factoryboy.fixture import register
from tests.factories import (
    GroupFactory,
    GroupSettingsFactory,
    MessageFactory,
    QuestionFactory,
    ReplyFactory,
    SessionFactory,
    SlackChannelFactory,
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
register(SlackSettingsFactory)
register(SlackTeamFactory)
register(SlackUserFactory)
register(TagFactory)
register(UserFactory)