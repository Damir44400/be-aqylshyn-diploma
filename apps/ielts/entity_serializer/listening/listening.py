from rest_framework import serializers

from apps.ielts import models
from .listening_question import IeltsListeningQuestionSerializer


class IeltsListeningSerializer(serializers.ModelSerializer):
    questions = IeltsListeningQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.IeltsListening
        fields = ("id", "title", "audio_file", "questions")
