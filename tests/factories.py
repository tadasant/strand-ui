import pytz

import factory
from django.contrib.auth.hashers import make_password

from app.groups.models import Group, GroupSettings
from app.messages.models import Message, Reply
from app.questions.models import Question, Session, Tag
from app.users.models import User
from app.slack.models import SlackSettings, SlackChannel, SlackUser, SlackTeam, SlackEvent


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


class GroupSettingsFactory(factory.DjangoModelFactory):
    class Meta:
        model = GroupSettings

    is_public = factory.Faker('pybool')
    group = factory.SubFactory(GroupFactory)


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Faker('word')


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question

    title = factory.Faker('sentence')
    description = factory.Faker('text')
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
    text = factory.Faker('sentence')
    session = factory.SubFactory(SessionFactory)
    author = factory.SubFactory(UserFactory)
    time = factory.Faker('date_time_this_decade', tzinfo=pytz.UTC)

    class Meta:
        model = Message


class ReplyFactory(factory.DjangoModelFactory):
    text = factory.Faker('sentence')
    message = factory.SubFactory(MessageFactory)
    author = factory.SubFactory(UserFactory)
    time = factory.Faker('date_time_this_decade', tzinfo=pytz.UTC)

    class Meta:
        model = Reply


class SlackEventFactory(factory.DjangoModelFactory):
    ts = str(factory.Faker('unix_time'))

    class Meta:
        model = SlackEvent


class SlackTeamFactory(factory.DjangoModelFactory):
    id = factory.Faker('md5')
    name = factory.Faker('name')
    group = factory.SubFactory(GroupFactory)

    class Meta:
        model = SlackTeam


class SlackSettingsFactory(factory.DjangoModelFactory):
    bot_token = factory.Faker('md5')
    slack_team = factory.SubFactory(SlackTeamFactory)

    class Meta:
        model = SlackSettings


class SlackChannelFactory(factory.DjangoModelFactory):
    id = factory.Faker('md5')
    name = factory.Faker('name')
    slack_team = factory.SubFactory(SlackTeamFactory)
    session = factory.SubFactory(SessionFactory)

    class Meta:
        model = SlackChannel


class SlackUserFactory(factory.DjangoModelFactory):
    id = factory.Faker('md5')
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

    class Meta:
        model = SlackUser