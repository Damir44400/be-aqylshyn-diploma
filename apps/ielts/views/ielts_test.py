from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import mixins
from rest_framework import viewsets

from apps.common import mixins as common_mixins
from apps.ielts import models as ielts_models
from apps.ielts import serializers as ielts_serializers


class IeltsTestViewSet(
    common_mixins.ActionSerializerMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializers = {
        "retrieve": ielts_serializers.IeltsTestDetailSerializer,
    }
    queryset = ielts_models.IeltsTest.objects.all()

    @extend_schema(
        responses=ielts_serializers.IeltsTestDetailSerializer,
        examples=[
            OpenApiExample(
                name="IeltsTestDetailExample",
                summary="Full test detail example",
                value={
                    "id": 1,
                    "name": "IELTS Test #1",
                    "readings": [
                        {
                            "id": 123,
                            "title": "About U",
                            "content": "Some reading passage goes here.",
                            "questions": [
                                {
                                    "id": 1001,
                                    "question_content": "What is the capital of France?",
                                    "question_type": "OPTIONS",
                                    "options": [
                                        {
                                            "id": 1002,
                                            "option": "France",
                                        },
                                        {
                                            "id": 1003,
                                            "option": "Germany",
                                        },
                                        {
                                            "id": 1004,
                                            "option": "Italy",
                                        },
                                        {
                                            "id": 1005,
                                            "option": "United Kingdom",
                                        }
                                    ],
                                },
                                {
                                    "id": 1002,
                                    "question_content": "What is your name?",
                                    "question_type": "FILL_BLANK",
                                    "options": [],
                                },
                                {
                                    "id": 1003,
                                    "question_content": "Insert words in the blanks",
                                    "question_type": "SELECT_INSERT_ANSWER",
                                    "options": ["Jane", "thank", "you", "too"],
                                }
                            ]
                        },
                    ],
                    "listenings": [
                        {
                            "id": 1,
                            "title": "About u",
                            "audio_file": "Bla bla bla",
                            "questions": [
                                {
                                    "id": 101,
                                    "question_content": "What is the capital of France?",
                                    "question_type": "OPTIONS",
                                    "options": [
                                        {
                                            "id": 1002,
                                            "option": "Paris",
                                        },
                                        {
                                            "id": 1003,
                                            "option": "Germany",
                                        },
                                        {
                                            "id": 1004,
                                            "option": "Italy",
                                        },
                                        {
                                            "id": 1005,
                                            "option": "United Kingdom",
                                        }
                                    ],
                                },
                                {
                                    "id": 102,
                                    "question_content": "What is your name?",
                                    "question_type": "FILL_BLANK",
                                    "options": []
                                }
                            ]
                        }
                    ],
                    "writings": [
                        {
                            "id": 789,
                            "title": "Sample writing task",
                            "description": "Describe the chart",
                            "images": []
                        }
                    ]
                },
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
