# Use of serializers limited to validating and saving models.

from rest_framework import serializers

from app.dialogues.models import Message, Reply
from app.topics.models import Discussion
from app.slack_integration.models import SlackEvent
from app.users.models import User


class MessageValidator(serializers.ModelSerializer):
    discussion_id = serializers.PrimaryKeyRelatedField(queryset=Discussion.objects.all(), source='discussion')
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author')
    origin_slack_event_id = serializers.PrimaryKeyRelatedField(queryset=SlackEvent.objects.all(),
                                                               source='origin_slack_event',
                                                               required=False)

    class Meta:
        model = Message
        fields = ('id', 'text', 'discussion_id', 'author_id', 'time', 'origin_slack_event_id')


class ReplyValidator(serializers.ModelSerializer):
    message_id = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), source='message')
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author')
    origin_slack_event_id = serializers.PrimaryKeyRelatedField(queryset=SlackEvent.objects.all(),
                                                               source='origin_slack_event',
                                                               required=False)

    class Meta:
        model = Reply
        fields = ('id', 'text', 'message_id', 'author_id', 'time', 'origin_slack_event_id')
