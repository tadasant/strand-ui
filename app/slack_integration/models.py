from django.db import models
from model_utils.models import TimeStampedModel

from app.questions.models import Session
from app.users.models import User
from app.groups.models import Group


class SlackTeam(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    group = models.OneToOneField(to=Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SlackUser(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
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

    def __str__(self):
        return f'{self.real_name or self.name}'


class SlackTeamInstallation(TimeStampedModel):
    slack_team = models.ForeignKey(to=SlackTeam, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    installer = models.ForeignKey(to=SlackUser, on_delete=models.CASCADE)
    bot_user_id = models.CharField(max_length=255)
    bot_access_token = models.CharField(max_length=255)
    help_channel_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'Installation for {self.slack_team.name}'


class SlackChannel(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    slack_team = models.ForeignKey(to=SlackTeam, on_delete=models.CASCADE)
    session = models.OneToOneField(to=Session, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'#{self.name}'


class SlackEvent(TimeStampedModel):
    ts = models.CharField(max_length=255)
