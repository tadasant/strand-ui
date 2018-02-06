import factory.fuzzy
import pytz
from django.contrib.auth.hashers import make_password

from app.dialogues.models import Message, Reply
from app.groups.models import Group
from app.slack_integration.models import (
    SlackAgent,
    SlackAgentStatus,
    SlackApplicationInstallation,
    SlackChannel,
    SlackEvent,
    SlackUser,
    SlackTeam
)
from app.topics.models import Topic, Discussion, Tag, DiscussionStatus
from app.users.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('safe_email')
    is_bot = factory.Faker('pybool')
    password = make_password('mypass123!')
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class GroupFactory(factory.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker('company')

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('word')


class TopicFactory(factory.DjangoModelFactory):
    class Meta:
        model = Topic

    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    is_anonymous = factory.Faker('pybool')

    original_poster = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)

    @factory.post_generation
    def tags(self, create, extracted):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class DiscussionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Discussion

    status = DiscussionStatus.OPEN.value
    time_start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    time_end = factory.Faker('future_datetime', tzinfo=pytz.UTC)
    topic = factory.SubFactory(TopicFactory)

    @factory.post_generation
    def participants(self, create, extracted):
        if not create:
            return

        if extracted:
            for participant in extracted:
                self.participants.add(participant)


class MessageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Message

    text = factory.Faker('sentence')
    discussion = factory.SubFactory(DiscussionFactory)
    author = factory.SubFactory(UserFactory)
    time = factory.Faker('date_time_this_decade', tzinfo=pytz.UTC)


class ReplyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Reply

    text = factory.Faker('sentence')
    message = factory.SubFactory(MessageFactory)
    author = factory.SubFactory(UserFactory)
    time = factory.Faker('date_time_this_decade', tzinfo=pytz.UTC)


class SlackEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlackEvent

    ts = factory.Faker('unix_time')


class SlackAgentFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlackAgent

    group = factory.SubFactory(GroupFactory)
    discuss_channel_id = factory.Faker('md5')
    status = SlackAgentStatus.INITIATED.value


class SlackTeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlackTeam

    id = factory.Faker('md5')
    name = factory.Faker('name')
    slack_agent = factory.SubFactory(SlackAgentFactory)


class SlackChannelFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlackChannel

    id = factory.Faker('md5')
    name = factory.Faker('name')
    slack_team = factory.SubFactory(SlackTeamFactory)
    discussion = factory.SubFactory(DiscussionFactory)


class SlackUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlackUser

    id = factory.Faker('md5')
    name = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    real_name = factory.LazyAttribute(lambda x: f'{x.first_name} {x.last_name}')
    display_name = factory.Faker('user_name')
    email = factory.Faker('safe_email')
    avatar_72 = factory.Faker('image_url')
    is_bot = factory.Faker('pybool')
    is_admin = factory.Faker('pybool')

    slack_team = factory.SubFactory(SlackTeamFactory)
    user = factory.SubFactory(UserFactory)


class SlackApplicationInstallationFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlackApplicationInstallation

    slack_agent = factory.SubFactory(SlackAgentFactory)
    access_token = factory.Faker('md5')
    scope = factory.Faker('sentence')
    installer = factory.SubFactory(SlackUserFactory)
    bot_user_id = factory.Faker('md5')
    bot_access_token = factory.Faker('md5')
