from django.db import models
from model_utils.models import TimeStampedModel

from app.users.models import User


class Group(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(to=User)


class GroupSetting(TimeStampedModel):
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('group', 'name')
