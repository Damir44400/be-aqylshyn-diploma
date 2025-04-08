from rest_framework import serializers

from apps.general_english import models
from .reading_option import ReadingOptionSerializer


class ReadingQuestionSerializer(serializers.ModelSerializer):
    options = ReadingOptionSerializer(many=True)

    class Meta:
        model = models.ReadingQuestion
        fields = (
            'id',
            'context',
            "question",
            'image',
            'source',
            'options',
        )
