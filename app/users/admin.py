from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm

from app.users.models import User


class CustomUserCreationForm(UserCreationForm):
    def save(self, *args, **kwargs):
        user = super(CustomUserCreationForm, self).save(commit=False)
        if not user.email:
            user.email = None
        user.save()
        return user


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    add_form = CustomUserCreationForm
