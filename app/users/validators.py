# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.users.models import User


class UserValidator(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'avatar_url', 'is_bot')

    def create(self, validated_data):
        alias = User.objects.generate_random_alias(4)
        return User(**validated_data, alias=alias)
