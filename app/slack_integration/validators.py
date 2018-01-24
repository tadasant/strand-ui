# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.groups.models import Group
from app.questions.models import Session
from app.slack_integration.models import (
    SlackTeam,
    SlackUser,
    SlackChannel,
    SlackTeamInstallation
)
from app.users.models import User


class SlackTeamValidator(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source='group')

    class Meta:
        model = SlackTeam
        fields = ('id', 'name', 'group_id')


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
    session_id = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all(), source='session')

    class Meta:
        model = SlackChannel
        fields = ('id', 'name', 'slack_team_id', 'session_id')


class SlackTeamInstallationValidator(serializers.ModelSerializer):
    slack_team_id = serializers.PrimaryKeyRelatedField(queryset=SlackTeam.objects.all(), source='slack_team')
    installer_id = serializers.PrimaryKeyRelatedField(queryset=SlackUser.objects.all(), source='installer')

    class Meta:
        model = SlackTeamInstallation
        fields = ('slack_team_id', 'access_token', 'scope', 'installer_id', 'bot_user_id', 'bot_access_token',
                  'help_channel_id', 'is_active')
        required_fields = ('slack_team_id', 'access_token', 'scope', 'installer_id', 'bot_user_id', 'bot_access_token')
