from pytest_factoryboy import register

from tests.factories import (
    UserFactory,
    GroupFactory,
    GroupSettingsFactory,
    TagFactory,
    QuestionFactory,
    SessionFactory,
    MessageFactory,
    ReplyFactory
)

register(UserFactory)
register(GroupFactory)
register(GroupSettingsFactory)
register(TagFactory)
register(QuestionFactory)
register(SessionFactory)
register(MessageFactory)
register(ReplyFactory)