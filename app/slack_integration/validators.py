# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.topics.models import Discussion
from app.slack_integration.models import (
    SlackChannel,
    SlackTeam,
    SlackUser

)
from app.users.models import User


class SlackUserValidator(serializers.ModelSerializer):
    slack_team_id = serializers.PrimaryKeyRelatedField(queryset=SlackTeam.objects.all(), source='slack_team')
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')

    class Meta:
        model = SlackUser
        fields = ('id', 'name', 'first_name', 'last_name', 'real_name', 'display_name', 'email', 'avatar_72',
                  'is_bot', 'is_admin', 'slack_team_id', 'user_id')
        required_fields = ('id', 'name', 'real_name', 'display_name', 'avatar_72', 'is_bot', 'is_admin',
                           'slack_team_id', 'user_id')


class SlackChannelValidator(serializers.ModelSerializer):
    slack_team_id = serializers.PrimaryKeyRelatedField(queryset=SlackTeam.objects.all(), source='slack_team')
    discussion_id = serializers.PrimaryKeyRelatedField(queryset=Discussion.objects.all(), source='discussion')

    class Meta:
        model = SlackChannel
        fields = ('id', 'name', 'slack_team_id', 'discussion_id')
