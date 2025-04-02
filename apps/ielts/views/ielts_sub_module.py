from rest_framework import mixins
from rest_framework import viewsets

from apps.common import mixins as common_mixins
from apps.ielts import models as ielts_models
from apps.ielts import serializers as ielts_serializers


class IeltsSubModuleView(
    common_mixins.ActionSerializerMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializers = {
        "retrieve": ielts_serializers.IeltsSubModuleDetailSerializer,
    }

    queryset = ielts_models.IeltsModule.objects.all()
