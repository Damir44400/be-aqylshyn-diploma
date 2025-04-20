from rest_framework import serializers

from apps.ielts import models
from .reading_question import ReadingQuestionSerializer


class IeltsReadingSerializer(serializers.ModelSerializer):
    questions = ReadingQuestionSerializer(many=True)

    class Meta:
        model = models.IeltsReading
        fields = (
            "id",
            "passage_number",
            "title",
            "content",
            "questions",
        )