import random
import string

from apps.common.services import EmailService, RedisService
from apps.users import models as user_models


class AuthService:
    def register(self, data):
        return user_models.User.objects.create_user(**data)

    def send_otp(self, data):
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

        EmailService().smtp(
            subject="Password Reset Code",
            body=message,
            to=[email],
        )

    def verify_otp(self, data):
        email = data['email']
        otp = data['otp']

        redis_service = RedisService()
        stored_email = redis_service.get(otp)

        if not stored_email:
            return False

        if stored_email != email:
            return False

        redis_service.delete(otp)
        return True
