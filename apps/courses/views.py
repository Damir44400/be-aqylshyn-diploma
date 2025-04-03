from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common import mixins as common_mixins, enums
from apps.courses import models as courses_models
from apps.courses import serializers as course_serializers
from apps.courses.entity_serializers import general_english as course_general_english_serializers


class CourseViewSet(
    common_mixins.ActionSerializerMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializers = {
        "list": course_serializers.CourseSerializer,
        "retrieve": course_general_english_serializers.CourseGeneralEnglishRetrieveSerializer,
        "general_english_modules": course_general_english_serializers.CourseGeneralEnglishModuleSerializer
    }
    permission_classes = [IsAuthenticated]
    queryset = courses_models.Course.objects.all()

    @extend_schema(tags=["general-english"])
    @action(detail=True, methods=["get"], url_path="modules")
    def general_english_modules(self, request, pk=None):
        queryset = self.get_queryset()
        instance = queryset.filter(type=enums.CourseType.GENERAL_ENGLISH).filter(id=pk).first()
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Course not found"})
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)
