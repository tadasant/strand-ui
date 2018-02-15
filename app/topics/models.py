from enum import Enum

from django.conf import settings
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


class Topic(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    is_anonymous = models.BooleanField(default=False)

    original_poster = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='topics')
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
    def datetime_of_last_non_bot_message(self):
        last_non_bot_message = self.messages.filter(author__is_bot=False).order_by('time').last()
        if last_non_bot_message:
            return last_non_bot_message.time
        else:
            return self.time_start

    @property
    def minutes_since_last_non_bot_message(self):
        time_delta = timezone.now() - self.datetime_of_last_non_bot_message
        minutes = round(time_delta.seconds / 60, 2)
        return minutes

    @property
    def is_closed(self):
        return self.status == DiscussionStatus.CLOSED.value

    @property
    def is_pending_closed(self):
        return self.status == DiscussionStatus.PENDING_CLOSED.value

    @property
    def is_stale(self):
        return self.status == DiscussionStatus.STALE.value

    def standby_to_auto_close(self):
        self.mark_as_pending_closed()
        self.save()

        from app.topics.tasks import auto_close_pending_closed_discussion
        auto_close_pending_closed_discussion.apply_async(args=[self.id, self.datetime_of_last_non_bot_message],
                                                         countdown=settings.AUTO_CLOSE_DELAY)

    def can_mark_as_stale(self):
        if self.minutes_since_last_non_bot_message >= 30.0:
            return True
        else:
            return False

    @transition(field=status, source=[DiscussionStatus.STALE.value, DiscussionStatus.PENDING_CLOSED.value],
                target=DiscussionStatus.OPEN.value, custom={'button_name': 'Mark as Open'})
    def mark_as_open(self):
        pass

    @transition(field=status, source=DiscussionStatus.OPEN.value, target=DiscussionStatus.STALE.value,
                conditions=[can_mark_as_stale], custom={'button_name': 'Mark as Stale'})
    def mark_as_stale(self):
        pass

    @transition(field=status, source=DiscussionStatus.STALE.value, target=DiscussionStatus.PENDING_CLOSED.value,
                custom={'button_name': 'Mark as Pending Closed'})
    def mark_as_pending_closed(self):
        pass

    @transition(field=status, source='*', target=DiscussionStatus.CLOSED.value,
                custom={'button_name': 'Mark as Closed'})
    def mark_as_closed(self):
        self.time_end = timezone.now()

    def __str__(self):
        return f'Discussion for "{self.topic.title}"'
