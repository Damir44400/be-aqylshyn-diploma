from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.common import mixins as common_mixins
from apps.ielts import models as ielts_models, services
from apps.ielts import serializers as ielts_serializers
from apps.ielts.entity_models.ielts_test import IeltsTest


class IeltsViewSet(
    common_mixins.ActionSerializerMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = ielts_models.IeltsModule.objects.all()
    serializers = {
        "list": ielts_serializers.IeltsModuleSerializer,
        "test_detail": ielts_serializers.IeltsTestDetailSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses=ielts_serializers.IeltsTestDetailSerializer,
        examples=[
            OpenApiExample(
                name="IeltsTestDetailExample",
                summary="Full test detail example",
                value={
                    "id": 1,
                    "name": "IELTS Test #1",
                    "reading_passages": [
                        {
                            "id": 123,
                            "title": "About U",
                            "part": "Part",
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
                    "listening_parts": [
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
                    "writing_tasks": [
                        {
                            "id": 789,
                            "title": "Sample writing task",
                            "description": "Describe the chart",
                            "images": []
                        }
                    ],
                    "speaking_parts": [
                        {
                            "id": 1,
                            "part": "Part",
                            "speaking_questions": [
                                {
                                    "id": 1001,
                                    "question": "What is the capital of France?",
                                    "additional_information": "What is the capital of France?",
                                }
                            ]
                        }
                    ]
                },
            )
        ]
    )
    @action(detail=False, methods=["get"], url_path="test/(?P<test_id>[^/.]+)")
    def test_detail(self, request, test_id):
        test = ielts_models.IeltsTest.objects.filter(pk=test_id).first()
        if not test:
            raise ValidationError("Test not found")
        serializer = self.get_serializer(test)
        return Response(serializer.data)


class IeltsTestSubmitViewSet(
    common_mixins.ActionSerializerMixin,
    viewsets.GenericViewSet
):
    queryset = IeltsTest.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    serializers = {
        "writing_submit": ielts_serializers.IeltsWritingSubmit,
        "speaking_submit": ielts_serializers.IeltsSpeakingSubmit,
        "reading_submit": ielts_serializers.IeltsReadingSubmit,
        "listening_submit": ielts_serializers.IeltsListeningSubmit,
    }

    _service = services.IeltsSubmitService()

    @action(detail=True, methods=["post"], url_path="writing-submit")
    def writing_submit(self, request, pk: int = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score = self._service.writing_submit(pk, serializer.validated_data, request.user)
        return Response({"score": score}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="speaking-submit")
    def speaking_submit(self, request, pk: int = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score = self._service.speaking_submit(pk, serializer.validated_data, request.user)
        return Response({"score": score}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="reading-submit")
    def reading_submit(self, request, pk: int = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score = self._service.reading_submit(pk, serializer.validated_data, request.user)
        return Response({"score": score}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="listening-submit")
    def listening_submit(self, request, pk: int = None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score = self._service.listening_submit(pk, serializer.validated_data, request.user)
        return Response({"score": score}, status=status.HTTP_201_CREATED)
