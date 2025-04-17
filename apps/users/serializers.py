from rest_framework import serializers

from apps.common import enums
from apps.courses import models as course_models
from apps.general_english import models as general_english_models
from apps.general_english import serializers as general_english_serializers
from apps.users import models as user_models


class UserSerializer(serializers.ModelSerializer):
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = user_models.User
        fields = (
            "id",
            "profile_picture",
            "first_name",
            "email",
            "is_staff",
            "user_progress"
        )

    def get_user_progress(self, obj):
        course = course_models.Course.objects.filter(type=enums.CourseType.GENERAL_ENGLISH).all()
        user_progress = general_english_models.UserProgress.objects.filter(course__in=course).all()
        return general_english_serializers.UserProgressSerializer(user_progress, many=True).data


class UserUpdateSerializer(serializers.ModelSerializer):
    last_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = user_models.User
        fields = (
            "id",
            "first_name",
            "profile_picture",
            "last_password",
            "password",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("partial", True)
        super(UserUpdateSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        user = self.instance
        last_password = attrs.get("last_password")
        password = attrs.get("password")
        password2 = attrs.get("password2")

        if password or password2:
            if not last_password:
                raise serializers.ValidationError(
                    {"last_password": "Current password is required to change the password."})

            if not user.check_password(last_password):
                raise serializers.ValidationError({"last_password": "Current password is incorrect."})

            if password != password2:
                raise serializers.ValidationError({"detail": "Passwords must match."})

        attrs.pop("password2", None)
        return attrs
