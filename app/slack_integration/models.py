from django.db import models
from django_fsm import FSMField, transition
from model_utils.models import TimeStampedModel

from app.questions.models import Session
from app.users.models import User
from app.groups.models import Group


class SlackAgent(TimeStampedModel):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='slack_agent', primary_key=True)
    # INITIATED, AUTHENTICATED, ACTIVE, PAUSED, INACTIVE
    status = FSMField(default='INITIATED', protected=True)
    help_channel_id = models.CharField(max_length=255, blank=True, null=True)

    def create_slack_application_installation_from_oauth(self, oauth_info):
        slack_user = SlackUser.objects.get(id=oauth_info['user_id'])
        slack_application_installation = SlackApplicationInstallation.objects.create(slack_agent=self,
                                                                                     access_token=oauth_info[
                                                                                         'access_token'],
                                                                                     scope=oauth_info['scope'],
                                                                                     installer=slack_user,
                                                                                     bot_user_id=oauth_info['bot'][
                                                                                         'bot_user_id'],
                                                                                     bot_access_token=oauth_info[
                                                                                         'bot']['bot_access_token'])
        return slack_application_installation

    def can_authenticate(self):
        if self.slack_application_installation:
            return True
        else:
            return False

    @transition(status, source=['INITIATED', 'INACTIVE'], target='AUTHENTICATED', conditions=[can_authenticate])
    def authenticate(self):
        pass

    def can_activate(self):
        if self.help_channel_id:
            return True
        else:
            return False

    @transition(field=status, source=['AUTHENTICATED', 'PAUSED', 'INACTIVE'], target='ACTIVE',
                conditions=[can_activate])
    def activate(self):
        pass

    @transition(field=status, source=['ACTIVE'], target='PAUSED')
    def pause(self):
        pass

    @transition(field=status, source=['ACTIVE', 'PAUSED'], target='INACTIVE')
    def inactivate(self):
        pass

    def __str__(self):
        return f'Slack Agent for {self.group.name}'


class SlackTeam(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    slack_agent = models.OneToOneField(to=SlackAgent, on_delete=models.CASCADE, related_name='slack_team')

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

    slack_team = models.ForeignKey(SlackTeam, on_delete=models.CASCADE, related_name='slack_users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slack_users')

    def __str__(self):
        return f'{self.real_name or self.name}'


class SlackApplicationInstallation(TimeStampedModel):
    slack_agent = models.OneToOneField(to=SlackAgent, on_delete=models.CASCADE,
                                       related_name='slack_application_installation')
    access_token = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    installer = models.OneToOneField(to=SlackUser, on_delete=models.CASCADE)
    bot_user_id = models.CharField(max_length=255)
    bot_access_token = models.CharField(max_length=255)

    def __str__(self):
        return f'Installation for {self.slack_agent.slack_team.name}'


class SlackChannel(TimeStampedModel):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    slack_team = models.ForeignKey(to=SlackTeam, on_delete=models.CASCADE, related_name='slack_channels')
    session = models.OneToOneField(to=Session, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'#{self.name}'


class SlackEvent(TimeStampedModel):
    ts = models.CharField(max_length=255)
