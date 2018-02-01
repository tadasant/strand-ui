from enum import Enum

from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel

from app.users.models import User
from app.groups.models import Group


class Tag(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Topic(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    is_anonymous = models.BooleanField(default=False)

    original_poster = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='asked_topics')
    group = models.ForeignKey(to=Group, on_delete=models.SET_NULL, null=True)

    tags = models.ManyToManyField(to=Tag, related_name='topics')

    def add_or_create_tags(self, tags):
        for tag_data in tags:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            self.tags.add(tag)

    def __str__(self):
        return f'"{self.title}"'


class DiscussionStatus(Enum):
    OPEN = 'OPEN'
    STALE = 'STALE'
    PENDING_CLOSED = 'PENDING CLOSED'
    CLOSED = 'CLOSED'


class Discussion(TimeStampedModel):
    time_start = models.DateTimeField(default=timezone.now)
    time_end = models.DateTimeField(null=True)
    status = FSMField(default=DiscussionStatus.OPEN.value, protected=True)
    topic = models.OneToOneField(to=Topic, on_delete=models.CASCADE)
    participants = models.ManyToManyField(to=User, related_name='discussions')

    @property
    def is_closed(self):
        return self.status == DiscussionStatus.CLOSED.value

    # TODO: Check timestamp of last non-bot message.
    def can_mark_as_stale(self):
        return True

    @transition(field=status, source=DiscussionStatus.OPEN.value, target=DiscussionStatus.STALE.value,
                conditions=[can_mark_as_stale])
    def mark_as_stale(self):
        pass

    @transition(field=status, source=DiscussionStatus.STALE.value, target=DiscussionStatus.PENDING_CLOSED.value)
    def mark_as_pending_closed(self):
        pass

    # TODO: Check timestamp of last non-bot message and PENDING CLOSED
    @transition(field=status, source='*', target=DiscussionStatus.CLOSED.value)
    def mark_as_closed(self):
        self.time_end = timezone.now()

    def __str__(self):
        return f'Discussion for "{self.topic.title}"'
