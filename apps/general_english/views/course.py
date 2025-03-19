from rest_framework import viewsets

from apps.common import mixins as common_mixins
from apps.general_english import models as general_english_models
from apps.general_english import serializers as general_english_serializers


class CourseViewSet(
    common_mixins.ActionPermissionMixin,
    common_mixins.ActionSerializerMixin,
    viewsets.GenericViewSet
):
    serializers = {
        "list":  general_english_serializers.CourseSerializer,
        "retrieve": general_english_serializers.CourseSerializer,
    }

    queryset = general_english_models.Course.objects.all()


