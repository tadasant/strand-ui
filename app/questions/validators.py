# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.groups.models import Group
from app.questions.models import Question, Session, Tag
from app.users.models import User


class TagValidator(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class QuestionValidator(serializers.ModelSerializer):
    original_poster_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='original_poster')
    solver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='solver', required=False)
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), source='group')

    class Meta:
        model = Question
        fields = ('title', 'description', 'status', 'is_anonymous', 'original_poster_id', 'solver_id', 'group_id')


class SessionValidator(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')

    class Meta:
        model = Session
        fields = ('id', 'status', 'time_start', 'time_end', 'question_id')
