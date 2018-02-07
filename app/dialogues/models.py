from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel

from app.topics.models import Discussion
from app.slack_integration.models import SlackEvent
from app.users.models import User


class Message(TimeStampedModel):
    text = models.TextField()
    discussion = models.ForeignKey(to=Discussion, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='messages')
    time = models.DateTimeField()
    origin_slack_event = models.ForeignKey(to=SlackEvent, on_delete=models.SET_NULL, related_name='message',
                                           blank=True, null=True)

    def __str__(self):
        return f'Message on {self.time}'


class Reply(TimeStampedModel):
    text = models.TextField()
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='replies')
    time = models.DateTimeField()
    origin_slack_event = models.OneToOneField(to=SlackEvent, on_delete=models.SET_NULL, related_name='reply',
                                              blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Replies'

    def __str__(self):
        return f'Reply on {self.time}'


@receiver(post_save, sender=Message)
def update_discussion_status_from_message(sender, instance=None, created=False, **kwargs):
    """Mark discussion as open if message is created.

    Fires on post_save signal for messages. Only marks
    a discussion as open if it is currently stale or
    pending closed.
    """
    if created:
        if instance.discussion.is_stale or instance.discussion.is_pending_closed:
            instance.discussion.mark_as_open()
            instance.discussion.save()


@receiver(post_save, sender=Reply)
def update_discussion_status_from_reply(sender, instance=None, created=False, **kwargs):
    """Mark discussion as open if reply is created.

    Fires on post_save signal for replies. Only marks
    a discussion as open if it is currently stale or
    pending closed.
    """
    if created:
        if instance.message.discussion.is_stale or instance.message.discussion.is_pending_closed:
            instance.message.discussion.mark_as_open()
            instance.message.discussion.save()
