from rest_framework import mixins
from rest_framework import viewsets

from apps.common import mixins as common_mixins
from apps.ielts import models as ielts_models
from apps.ielts import serializers as ielts_serializers


class IeltsView(
    common_mixins.ActionSerializerMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializers = {
        "list": ielts_serializers.IeltsModuleSerializer,
        "retrieve": ielts_serializers.IeltsModuleDetailSerializer,
    }

    queryset = ielts_models.IeltsModule.objects.all()
