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
        "request_to_reset_password": auth_serializers.SendOTPSerializer,
        "verify_request_to_reset_password": auth_serializers.VerifyOTPSerializer,
        "reset_password": auth_serializers.ResetPasswordSerializer,
    }

    service = auth_services.AuthService()

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.register(serializer.validated_data)
        return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)

    @extend_schema(tags=["reset password"])
    @action(detail=False, methods=["post"], url_path="request_to_reset_password")
    def request_to_reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.service.send_otp(serializer.validated_data)
        return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)

    @extend_schema(tags=["reset password"])
    @action(detail=False, methods=["post"], url_path="verify_request_to_reset_password")
    def verify_request_to_reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_token = self.service.verify_otp(serializer.validated_data)

        response = Response(
            {"detail": "OTP verified successfully", "session_token": session_token},
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            key="SESSION-TOKEN",
            value=session_token,
            httponly=True,
            secure=True,
            max_age=3600
        )
        return response

    @extend_schema(tags=["reset password"])
    @action(detail=False, methods=["post"], url_path="reset-password")
    def reset_password(self, request, *args, **kwargs):
        session_token = request.COOKIES.get("SESSION-TOKEN")

        if not session_token:
            return Response(
                {"detail": "Session token is missing or invalid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.service.reset_password(serializer.validated_data, session_token)

        return Response({"detail": "Password reset successfully"}, status=status.HTTP_200_OK)
