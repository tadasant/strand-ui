from django.db import models
from model_utils.models import TimeStampedModel

from app.questions.models import Session
from app.slack_integration.models import SlackEvent
from app.users.models import User


class Message(TimeStampedModel):
    text = models.TextField()
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE, related_name='messages')
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
