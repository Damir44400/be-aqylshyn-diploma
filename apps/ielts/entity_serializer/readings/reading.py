from rest_framework import serializers

from apps.ielts import models
from .reading_question import ReadingQuestionSerializer


class IeltsReadingSerializer(serializers.ModelSerializer):
    questions = ReadingQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.IeltsReading
        fields = (
            "id",
            "title",
            "content",
            "questions",
        )
