from django.db import models
from model_utils.models import TimeStampedModel

from app.questions.models import Session
from app.users.models import User
from app.groups.models import Group


class SlackTeam(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    group = models.OneToOneField(to=Group, on_delete=models.CASCADE)


class SlackSettings(TimeStampedModel):
    bot_token = models.CharField(max_length=255, null=True)
    slack_team = models.OneToOneField(to=SlackTeam, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Slack settings'


class SlackChannel(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    slack_team = models.ForeignKey(to=SlackTeam, on_delete=models.CASCADE)
    session = models.OneToOneField(to=Session, on_delete=models.CASCADE, null=True)


class SlackUser(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    real_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)
    avatar_72 = models.CharField(max_length=255)
    is_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    slack_team = models.ForeignKey(SlackTeam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SlackEvent(TimeStampedModel):
    ts = models.CharField(max_length=255)
