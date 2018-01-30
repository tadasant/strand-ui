from enum import Enum

from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel

from app.groups.models import Group
from app.users.models import User


class Tag(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class QuestionStatus(Enum):
    UNSOLVED = 'UNSOLVED'
    SOLVED = 'SOLVED'


class Question(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    status = FSMField(default=QuestionStatus.UNSOLVED.value, protected=True)
    is_anonymous = models.BooleanField(default=False)

    original_poster = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='asked_questions')
    solver = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='solved_questions')
    group = models.ForeignKey(to=Group, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField(to=Tag, related_name='questions')

    def can_mark_as_solved(self):
        return self.session.is_closed

    @transition(field=status, source=QuestionStatus.UNSOLVED.value, target=QuestionStatus.SOLVED.value)
    def mark_as_solved(self):
        pass

    def add_or_create_tags(self, tags):
        for tag_data in tags:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            self.tags.add(tag)

    def __str__(self):
        return f'"{self.title}"'


class SessionStatus(Enum):
    OPEN = 'OPEN'
    STALE = 'STALE'
    PENDING_CLOSED = 'PENDING CLOSED'
    CLOSED = 'CLOSED'


class Session(TimeStampedModel):
    time_start = models.DateTimeField(default=timezone.now)
    time_end = models.DateTimeField(null=True)
    status = FSMField(default=SessionStatus.OPEN.value, protected=True)
    question = models.OneToOneField(to=Question, on_delete=models.CASCADE)
    participants = models.ManyToManyField(to=User, related_name='sessions')

    @property
    def datetime_of_last_non_bot_message(self):
        last_non_bot_message = self.messages.filter(author__is_bot=False).order_by('time').first()
        if last_non_bot_message:
            return last_non_bot_message.time
        else:
            return self.time_start

    @property
    def minutes_since_last_non_bot_message(self):
        time_delta = timezone.now() - self.datetime_of_last_non_bot_message
        minutes = round(time_delta.seconds / 60)
        return minutes

    @property
    def is_closed(self):
        return self.status == SessionStatus.CLOSED.value

    @property
    def is_stale(self):
        return self.status == SessionStatus.STALE.value

    def can_mark_as_stale(self):
        if self.minutes_since_last_non_bot_message > 30:
            return True
        else:
            return False

    @transition(field=status, source=SessionStatus.OPEN.value, target=SessionStatus.STALE.value,
                conditions=[can_mark_as_stale])
    def mark_as_stale(self):

        pass

    @transition(field=status, source=SessionStatus.STALE.value, target=SessionStatus.PENDING_CLOSED.value)
    def mark_as_pending_closed(self):
        from app.questions.tasks import close_pending_closed_session
        close_pending_closed_session.apply_async(args=[self.id, self.datetime_of_last_non_bot_message],
                                                 countdown=60 * 5)

    @transition(field=status, source='*', target=SessionStatus.CLOSED.value)
    def mark_as_closed(self):
        self.time_end = timezone.now()

    def __str__(self):
        return f'Session for "{self.question.title}"'
