from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.common import mixins as common_mixins
from apps.ielts import models as ielts_models
from apps.ielts import serializers as ielts_serializers


class IeltsViewSet(
    common_mixins.ActionSerializerMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = ielts_models.IeltsModule.objects.all()
    serializers = {
        "list": ielts_serializers.IeltsModuleSerializer,
        "list_submodules": ielts_serializers.IeltsModuleDetailSerializer,
        "test_detail": ielts_serializers.IeltsTestDetailSerializer,
    }

    @action(detail=True, methods=["get"], url_path="submodules")
    def list_submodules(self, request, pk=None):
        module = self.get_object()
        submodules = module.sub_modules.all()
        serializer = ielts_serializers.IeltsSubModuleDetailSerializer(submodules, many=True)
        return Response(serializer.data)

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
    @action(detail=True, methods=["get"], url_path="submodules/(?P<submodule_id>[^/.]+)/tests/(?P<test_id>[^/.]+)")
    def test_detail(self, request, pk=None, submodule_id=None, test_id=None):
        test = ielts_models.IeltsTest.objects.filter(pk=test_id, sub_model_id=submodule_id).first()
        if not test:
            raise ValidationError("Test not found")
        serializer = self.get_serializer(test)
        return Response(serializer.data)
