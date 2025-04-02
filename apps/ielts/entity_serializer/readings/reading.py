from drf_spectacular import openapi
from rest_framework import serializers

from apps.common import enums
from apps.ielts import models
from .reading_question import ReadingQuestionSerializer


class IeltsReadingSerializer(serializers.ModelSerializer):
    questions = ReadingQuestionSerializer(read_only=True)

    class Meta:
        model = models.IeltsReading
        fields = (
            "id",
            "title",
            "content",
            "questions",
        )

    swagger_schema_fields = {
        "title": "About u",
        "content": "Bla bla bla",
        'questions': [
            {
                'question_content': openapi.OpenApiExample(
                    name="question_content",
                    value="What is the capital of France?"
                ),
                'question_type': openapi.OpenApiExample(
                    name="question_type",
                    value=enums.IeltsReadingQuestionType.OPTIONS,
                ),
                'options': openapi.OpenApiExample(
                    name="options",
                    value=["Option A: Paris", "Option B: London", "Option C: Berlin"],
                ),
            },
            {
                'question_content': openapi.OpenApiExample(
                    name="question_content",
                    value="What is your name?"
                ),
                'question_type': openapi.OpenApiExample(
                    name="question_type",
                    value=enums.IeltsReadingQuestionType.FILL_BLANK,
                ),
                'options': openapi.OpenApiExample(
                    name="options",
                    value=[],
                ),
            },
            {
                'question_content': openapi.OpenApiExample(
                    name="question_content",
                    value="Insert the words to needed places\nHello _\n How are _?\nI am fine _ _"
                ),
                'question_type': openapi.OpenApiExample(
                    name="question_type",
                    value=enums.IeltsReadingQuestionType.SELECT_INSERT_ANSWER,
                ),
                'options': openapi.OpenApiExample(
                    name="options",
                    value=["Jane", "thank", "you", "too"]
                ),
            }
        ]
    }
