from django.db import models
from model_utils.models import TimeStampedModel

from app.users.models import User


class Group(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(to=User)


class GroupSettings(TimeStampedModel):
    is_public = models.BooleanField(default=True)
    group = models.OneToOneField(to=Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Group Settings'
