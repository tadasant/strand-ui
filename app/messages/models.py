from django.db import models
from model_utils.models import TimeStampedModel

from app.questions.models import Session
from app.users.models import User


class Message(TimeStampedModel):
    text = models.TextField()
    session = models.ForeignKey(to=Session, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time = models.DateTimeField()


class Reply(TimeStampedModel):
    text = models.TextField()
    message = models.ForeignKey(to=Message, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time = models.DateTimeField()