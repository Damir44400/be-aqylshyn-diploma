from drf_spectacular import openapi
from rest_framework import serializers

from apps.common import enums
from apps.ielts import models
from .listening_question import IeltsListeningQuestionSerializer

class IeltsListeningSerializer(serializers.ModelSerializer):
    questions = IeltsListeningQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.IeltsListening
        fields = (
            "id",
            "title",
            "audio_file",
            "questions",
        )

        swagger_schema_fields = {
            "title": "About u",
            "audio_file": "Bla bla bla",
            'questions': [
                {
                    'question_content': openapi.OpenApiExample(
                        name="question_content",
                        value="What is the capital of France?"
                    ),
                    'question_type': openapi.OpenApiExample(
                        name="question_type",
                        value=enums.IeltsListeningQuestionType.OPTIONS,
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
                        value=enums.IeltsListeningQuestionType.FILL_BLANK,
                    ),
                    'options': openapi.OpenApiExample(
                        name="options",
                        value=[],
                    ),
                },
            ]
        }
