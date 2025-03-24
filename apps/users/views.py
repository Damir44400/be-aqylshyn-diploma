from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common import mixins as common_mixins
from apps.general_english import serializers as general_serializers
from apps.users import models as user_models
from apps.users import serializers as user_serializers
from apps.users import services as user_services


# Create your views here.
class UserViewSet(
    common_mixins.ActionSerializerMixin,
    common_mixins.ActionPermissionMixin,
    viewsets.GenericViewSet,
):
    queryset = user_models.User.objects.all()
    serializers = {
        "me": user_serializers.UserSerializer,
        "me_update": user_serializers.UserUpdateSerializer,
        "get_user_progresses": general_serializers.UserProgressSerializer
    }

    serializer_class = user_serializers.UserSerializer
    service = user_services.UserService()

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=["patch"], url_path="profile")
    def me_update(self, request):
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            self.service.update(user, serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'], url_path='my-courses/progresses')
    def get_user_progresses(self, request):
        user = self.request.user
        queryset = self.queryset.prefetch_related("user_progresses").all()
        user_progresses = queryset.filter(user_progresses__user=user)
        serializer = self.get_serializer(user_progresses, many=True)
        return Response(serializer.data)
