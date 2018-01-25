import pytz

import factory
import factory.fuzzy
from django.contrib.auth.hashers import make_password

from app.groups.models import Group
from app.discussions.models import Message, Reply
from app.questions.models import Question, Session, Tag
from app.users.models import User
from app.slack_integration.models import SlackApplicationInstallation, SlackChannel, SlackEvent, SlackUser, SlackTeam


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('safe_email')
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


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    is_solved = factory.Faker('pybool')
    is_anonymous = factory.Faker('pybool')

    original_poster = factory.SubFactory(UserFactory)
    solver = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)

    @factory.post_generation
    def tags(self, create, extracted):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class SessionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Session

    time_start = factory.Faker('past_datetime', tzinfo=pytz.UTC)
    time_end = factory.Faker('future_datetime', tzinfo=pytz.UTC)
    question = factory.SubFactory(QuestionFactory)

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
    session = factory.SubFactory(SessionFactory)
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


class SlackTeamFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlackTeam

    id = factory.Faker('md5')
    name = factory.Faker('name')
    group = factory.SubFactory(GroupFactory)


class SlackChannelFactory(factory.DjangoModelFactory):
    class Meta:
        model = SlackChannel

    id = factory.Faker('md5')
    name = factory.Faker('name')
    slack_team = factory.SubFactory(SlackTeamFactory)
    session = factory.SubFactory(SessionFactory)


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

    slack_team = factory.SubFactory(SlackTeamFactory)
    access_token = factory.Faker('md5')
    scope = factory.Faker('sentence')
    installer = factory.SubFactory(SlackUserFactory)
    bot_user_id = factory.Faker('md5')
    bot_access_token = factory.Faker('md5')
    help_channel_id = factory.Faker('md5')
    is_active = factory.Faker('pybool')
