from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def create_user_from_slack_user(self, slack_user):
        email = self.normalize_email(slack_user.email)
        username = self.model.normalize_username(slack_user.display_name or slack_user.name)
        first_name = slack_user.first_name
        last_name = slack_user.last_name
        avatar_url = slack_user.avatar_72
        user = self.model(email=email, username=username, first_name=first_name,
                          last_name=last_name, avatar_url=avatar_url)
        user.set_password(None)
        user.save(using=self._db)

        slack_user.slack_team.group.members.add(user)

        slack_user.user = user
        slack_user.save()

        return user
