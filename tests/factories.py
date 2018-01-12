import factory
from app.groups.models import Group, GroupSettings
from app.messages.models import Message, Reply
from app.questions.models import Question, Session, Tag
from app.users.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker('safe_email')
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class GroupFactory(factory.Factory):
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


class GroupSettingsFactory(factory.Factory):
    class Meta:
        model = GroupSettings

    is_public = factory.Faker('pybool')
    group = factory.SubFactory(GroupFactory)


class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = factory.Faker('word')


class QuestionFactory(factory.Factory):
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


class SessionFactory(factory.Factory):
    class Meta:
        model = Session

    time_start = factory.Faker('past_datetime')
    time_end = factory.Faker('future_datetime')
    question = factory.SubFactory(QuestionFactory)

    @factory.post_generation
    def participants(self, create, extracted):
        if not create:
            return

        if extracted:
            for participant in extracted:
                self.participants.add(participant)


class MessageFactory(factory.Factory):
    text = factory.Faker('text')
    session = factory.SubFactory(SessionFactory)
    author = factory.SubFactory(UserFactory)
    time = factory.Faker('date_time_this_decade')

    class Meta:
        model = Message


class ReplyFactory(factory.Factory):
    text = factory.Faker('text')
    message = factory.SubFactory(MessageFactory)
    author = factory.SubFactory(UserFactory)
    time = factory.Faker('date_time_this_decade')

    class Meta:
        model = Reply
