from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm

from app.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
