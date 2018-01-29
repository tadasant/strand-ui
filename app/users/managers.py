from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def create_user_from_slack_user(self, slack_user):
        email = self.normalize_email(slack_user.email)
        username = self.model.normalize_username(slack_user.display_name or slack_user.name)
        user = self.model(email=email, username=username, first_name=slack_user.first_name,
                          last_name=slack_user.last_name, avatar_url=slack_user.avatar_72, is_bot=slack_user.is_bot)
        user.set_password(None)
        user.save(using=self._db)

        slack_user.slack_team.slack_agent.group.members.add(user)

        slack_user.user = user
        slack_user.save()

        return user
