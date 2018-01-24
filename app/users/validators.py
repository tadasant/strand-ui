# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.users.models import User


class UserValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'avatar_url')
