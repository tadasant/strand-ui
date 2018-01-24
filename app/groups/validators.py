# Use of serializers limited to validating and saving models.

from rest_framework import serializers

from app.groups.models import Group


class GroupValidator(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
