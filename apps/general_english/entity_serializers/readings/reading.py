from rest_framework import serializers

from apps.general_english import models
from .reading_question import ReadingQuestionSerializer


class ReadingSerializer(serializers.ModelSerializer):
    questions = ReadingQuestionSerializer(many=True, source="reading_questions")

    class Meta:
        model = models.Reading
        fields = (
            'id',
            'context',
            'image',
            'source',
            'questions',
        )
