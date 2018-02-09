from random import choice
from string import digits

from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        super().create_user(username, email=email, password=password, alias=self.generate_random_alias(4),
                            **extra_fields)

    def create_user_from_slack_user(self, slack_user):
        email = self.normalize_email(slack_user.email)
        username = self.model.normalize_username(slack_user.display_name or slack_user.name)
        user = self.model(email=email, username=username, first_name=slack_user.first_name,
                          last_name=slack_user.last_name, avatar_url=slack_user.avatar_72, is_bot=slack_user.is_bot,
                          alias=self.generate_random_alias(4))
        user.set_password(None)
        user.save(using=self._db)

        slack_user.slack_team.slack_agent.group.members.add(user)

        slack_user.user = user
        slack_user.save()

        return user

    def generate_random_alias(self, length=4):
        alias = 'anonymous-user-' + ''.join([choice(digits) for i in range(length)])

        if self.model.objects.filter(alias=alias).exists():
            return self.generate_random_alias(4)
        else:
            return alias
