from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_('username'), max_length=150,
                                help_text=_('150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                validators=[username_validator])
    email = models.EmailField(_('email address'), blank=True, null=True, unique=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        user = super(User, self).save(*args, **kwargs)
        return user

