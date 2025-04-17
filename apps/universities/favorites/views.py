from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apps.common import mixins as common_mixins
from apps.common import serializers as common_serializers
from .models import Favorite
from .serializers import FavoriteCreateSerializer, FavoriteSerializer


# Create your views here.
@extend_schema(tags=["favorites"])
class FavoriteViewSet(
    common_mixins.ActionSerializerMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializers = {
        "create": FavoriteCreateSerializer,
        "destroy": common_serializers.BlankSerializer,
        "list": FavoriteSerializer,
    }
    permission_classes = (IsAuthenticated,)
    queryset = Favorite.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
