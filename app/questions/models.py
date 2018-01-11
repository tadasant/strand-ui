from datetime import datetime

from django.db import models
from model_utils.models import TimeStampedModel

from app.users.models import User
from app.groups.models import Group


class Tag(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)


class Question(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_solved = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)

    original_poster = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='asked_questions')
    solver = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, null=True, related_name='solved_questions')
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)

    tags = models.ManyToManyField(to=Tag)


class Session(TimeStampedModel):
    time_start = models.DateTimeField(default=datetime.now())
    time_end = models.DateTimeField(null=True)
    question = models.OneToOneField(to=Question, on_delete=models.CASCADE)
