from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common import mixins as common_mixins
from apps.general_english import models as general_english_models
from apps.general_english import serializers as general_english_serializers


class ModuleViewSet(
    common_mixins.ActionSerializerMixin,
    viewsets.GenericViewSet,
):
    serializers = {
        'readings': general_english_serializers.ModuleReadingSerializer,
        "writing": general_english_serializers.ModuleWritingSerializer,
        "listening_questions": general_english_serializers.ModuleListeningSerializer,
        "speakings": general_english_serializers.ModuleSpeakingSerializer,
        "detail": general_english_serializers.ModuleSerializer,
    }

    permission_classes = (permissions.IsAuthenticated,)

    queryset = general_english_models.Module.objects.all()

    @extend_schema(tags=['general-english sections'])
    @action(detail=True, methods=['get'], url_path='readings')
    def readings(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(tags=['general-english sections'])
    @action(detail=True, methods=['get'], url_path='writing')
    def writing(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(tags=['general-english sections'])
    @action(detail=True, methods=['get'], url_path='listening-questions')
    def listening_questions(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(tags=['general-english sections'])
    @action(detail=True, methods=['get'], url_path='speakings')
    def speakings(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(tags=['general-english sections'])
    @action(detail=True, methods=['get'], url_path='detail')
    def detail(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
