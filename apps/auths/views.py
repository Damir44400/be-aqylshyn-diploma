from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.auths import serializers as auth_serializers
from apps.auths import services as auth_services
from apps.common import mixins as common_mixins

@extend_schema_view(
    send_otp=extend_schema(
        summary="Send otp when user forgot password",
    ),
    verify_otp=extend_schema(
        summary="Verify otp when user send otp",
    ),
)
class AuthView(common_mixins.ActionSerializerMixin, viewsets.GenericViewSet):
    serializers = {
        "register": auth_serializers.UserCreateSerializer,
        "send_otp": auth_serializers.SendOTPSerializer,
        "verify_otp": auth_serializers.VerifyOTPSerializer,
    }

    service = auth_services.AuthService()

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.register(serializer.validated_data)
        return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="send_otp")
    def send_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.send_otp(serializer.validated_data)
        return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="verify_otp")
    def verify_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_valid_otp = self.service.verify_otp(serializer.validated_data)
        if not is_valid_otp:
            return Response({"detail": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "OTP verified successfully"}, status=status.HTTP_200_OK)
