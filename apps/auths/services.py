import random
import string
import uuid

from rest_framework.exceptions import ValidationError

from apps.common.services import EmailService, RedisService
from apps.users import models as user_models


class AuthService:
    @staticmethod
    def register(data):
        return user_models.User.objects.create_user(**data)

    @staticmethod
    def send_otp(data):
        email = data['email']
        redis_service = RedisService()

        digits = string.digits
        generated_otp = ''.join(random.choice(digits) for _ in range(6))

        while redis_service.get(generated_otp):
            generated_otp = ''.join(random.choice(digits) for _ in range(6))

        redis_service.set(generated_otp, email)

        message = (
            f"Hello,\n\n"
            f"You have requested a password reset. Your OTP code is: {generated_otp}\n\n"
            f"If you did not request this code, you can safely ignore this email."
        )
        print(generated_otp)
        EmailService().smtp(
            subject="Password Reset Code",
            body=message,
            to=[email],
        )

    @staticmethod
    def verify_otp(data):
        email = data['email']
        otp = data['otp']

        redis_service = RedisService()
        stored_email = redis_service.get(otp)

        if not stored_email:
            raise ValidationError({"detail": "OTP code is invalid"})

        if stored_email != email:
            raise ValidationError({"detail": "OTP code is invalid"})

        redis_service.delete(otp)
        generate_session_token = uuid.uuid4().hex
        redis_service.set(f"session_token:{generate_session_token}", email, expire=360)

        return generate_session_token

    @staticmethod
    def reset_password(data, session_token):
        redis_service = RedisService()

        email = redis_service.get(f"session_token:{session_token}")
        if not email:
            raise ValidationError({"detail": "Session token is expired or invalid"})

        user = user_models.User.objects.filter(email=email).first()

        if not user:
            raise ValidationError({"detail": "User not found, please try again or contact with support."})

        user.set_password(data['password'])
        user.save()
        return user
