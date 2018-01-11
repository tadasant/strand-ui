import factory
from faker import Faker

from app.groups.models import Group, GroupSettings
from app.messages.models import Message, Reply
from app.questions.models import Question, Session, Tag
from app.users.models import User

fake = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = fake.safe_email()
    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()


class GroupFactory(factory.Factory):
    class Meta:
        model = Group

    name = fake.company()

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)


class GroupSettingsFactory(factory.Factory):
    class Meta:
        model = GroupSettings

    is_public = fake.pybool()
    group = factory.SubFactory(GroupFactory)


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = fake.word()


class QuestionFactory(factory.Factory):
    class Meta:
        model = Question

    title = fake.sentence()
    description = fake.text()
    is_solved = fake.pybool()
    is_anonymous = fake.pybool()

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


class SessionFactory(factory.Factory):
    time_start = fake.past_datetime()
    time_end = fake.future_datetime()
    question = factory.SubFactory(QuestionFactory)

    @factory.post_generation
    def participants(self, create, extracted):
        if not create:
            return

        if extracted:
            for participant in extracted:
                self.participants.add(participant)


class MessageFactory(factory.Factory):
    text = fake.text()
    session = factory.SubFactory(SessionFactory)
    author = factory.SubFactory(UserFactory)
    time = fake.date_time_this_decade()

    class Meta:
        model = Message


class ReplyFactory(factory.Factory):
    text = fake.text()
    message = factory.SubFactory(MessageFactory)
    author = factory.SubFactory(UserFactory)
    time = fake.date_time_this_decade()

    class Meta:
        model = Reply
