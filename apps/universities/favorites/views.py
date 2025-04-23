from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common import mixins as common_mixins
from apps.common import serializers as common_serializers
from .models import Favorite
from .serializers import FavoriteCreateSerializer, FavoriteSerializer
from .services import FavoriteService


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
    service = FavoriteService()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = self.service.insert_favorite(serializer.validated_data['university'], user=self.request.user)
        return Response({"message": message}, status=status.HTTP_200_OK)
