# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.groups.models import Group
from app.topics.models import Topic, Discussion, Tag
from app.users.models import User


class TagValidator(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class TopicValidator(serializers.ModelSerializer):
    original_poster_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='original_poster')
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source='group')

    class Meta:
        model = Topic
        fields = ('title', 'description', 'is_anonymous', 'original_poster_id', 'group_id')


class DiscussionValidator(serializers.ModelSerializer):
    topic_id = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), source='topic')

    class Meta:
        model = Discussion
        fields = ('id', 'status', 'time_start', 'time_end', 'topic_id')
