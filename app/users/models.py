from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar_url = models.CharField(max_length=255, null=True)
