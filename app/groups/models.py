from django.db import models
from model_utils.models import TimeStampedModel

from app.users.models import User


class Group(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(to=User)

    def __str__(self):
        return self.name
