# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.groups.models import Group


class GroupValidator(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
