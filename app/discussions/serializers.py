from rest_framework import serializers

from app.discussions.models import Message, Reply
from app.questions.models import Session
from app.users.models import User


class MessageSerializer(serializers.ModelSerializer):
    session_id = serializers.PrimaryKeyRelatedField(queryset=Session.objects.all(), source='session')
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author')

    class Meta:
        model = Message
        fields = ('id', 'text', 'session_id', 'author_id', 'time')


class ReplySerializer(serializers.ModelSerializer):
    message_id = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), source='message')
    author_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author')

    class Meta:
        model = Reply
        fields = ('id', 'text', 'message_id', 'author_id', 'time')
