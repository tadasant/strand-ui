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
    tags = TagValidator(many=True, required=False)

    class Meta:
        model = Question
        fields = ('title', 'description', 'is_solved', 'is_anonymous', 'original_poster_id', 'solver_id', 'group_id',
                  'tags')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        question = Question.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            question.tags.add(tag)
        return question


class SessionValidator(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')

    class Meta:
        model = Session
        fields = ('id', 'time_start', 'time_end', 'question_id')
