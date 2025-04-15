from rest_framework import serializers

from apps.common import enums
from apps.ielts import models
from .reading_options import ReadingOptionsSerializer, ReadingSelectInsertSerializer


class ReadingQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = models.IeltsReadingQuestion
        fields = (
            "id",
            "question_content",
            "question_type",
            "options",
        )

    def get_options(self, obj):
        if obj.question_type == enums.IeltsReadingQuestionType.OPTIONS:
            return ReadingOptionsSerializer(obj.options.all(), many=True).data

        elif obj.question_type == enums.IeltsReadingQuestionType.SELECT_INSERT_ANSWER:
            return ReadingSelectInsertSerializer(obj.select_insert_data, many=False).data

        return []
