from django.db import models
from model_utils.models import TimeStampedModel

from app.questions.models import Session
from app.slack.models import SlackEvent
from app.users.models import User


class Message(TimeStampedModel):
    text = models.TextField()
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    slack_event = models.ForeignKey(to=SlackEvent, on_delete=models.CASCADE, null=True)


class Reply(TimeStampedModel):
    text = models.TextField()
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    slack_event = models.ForeignKey(to=SlackEvent, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Replies'
