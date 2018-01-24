# Use of serializers limited to deserializing, validating and saving model instance data.

from rest_framework import serializers

from app.questions.models import Question, Session, Tag


class QuestionValidator(serializers.ModelSerializer):
    class Meta:
        model = Question


class SessionValidator(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'time_start', 'time_end', 'question_id')


class TagValidator(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
