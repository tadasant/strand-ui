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
        """Override __str__.

        AbstractUser uses self.get_username() for this. Since our username_field
        is email (nullable), this will throw errors in Django admin since we return
        None (not a string). To avoid this, we'll return username which is required
        even if not unique.
        """
        return self.username

    def save(self, *args, **kwargs):
        """Override save.

        We need to override save to prevent secondary effects of blank argument.
        Blank allows us to submit forms with an empty field. However, Django forms
        interpret blank to mean either Null or an empty string (''). While Null
        does not equal Null (our unique constraint passes), this is not the case
        with empty strings. To override this behavior, if email is an empty string
        we set it to None before saving the user.
        """
        if not self.email:
            self.email = None
        user = super(User, self).save(*args, **kwargs)
        return user

