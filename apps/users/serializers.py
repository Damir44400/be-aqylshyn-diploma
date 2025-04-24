from django.db.models import Sum
from rest_framework import serializers

from apps.common import enums
from apps.courses import models as course_models
from apps.general_english import models as ge_models
from apps.general_english import serializers as ge_serializers
from apps.ielts import models as ielts_models
from apps.users import models as user_models


class UserAchievementSerializer(serializers.Serializer):
    progress = serializers.SerializerMethodField()
    scores = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    def get_progress(self, obj):
        progress = self._get_user_progress()  # lazy-cache
        return progress.get_progress if progress else None

    def get_level(self, obj):
        progress = self._get_user_progress()
        return progress.level if progress else None

    def get_courses(self, obj):
        user = self._get_user()
        res = []

        if self._get_user_progress():
            res.append("General English")

        if ielts_models.IeltsTestSubmit.objects.filter(user=user).exists():
            res.append("IELTS")

        return res

    def get_scores(self, obj):
        user = self._get_user()
        if not user:
            return 0

        total = (
                    ge_models.ModuleScore
                    .objects
                    .filter(module__user_course__user=user)
                    .aggregate(total=Sum("score"))
                )["total"] or 0

        return total

    def _get_user(self):
        return getattr(self.context.get("request"), "user", None)

    def _get_user_progress(self):
        if not hasattr(self, "_cached_progress"):
            user = self._get_user()
            self._cached_progress = (
                ge_models.UserProgress.objects
                .select_related("course")
                .filter(user=user)
                .first()
            )
        return self._cached_progress


class UserSerializer(serializers.ModelSerializer):
    achievement = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = user_models.User
        fields = (
            "id",
            "profile_picture",
            "first_name",
            "email",
            "is_staff",
            "achievement",
            "user_progress",
        )

    def get_achievement(self, obj):
        return UserAchievementSerializer(instance=obj, context=self.context).data

    def get_user_progress(self, obj):
        ge_course_ids = (
            course_models.Course.objects
            .filter(type=enums.CourseType.GENERAL_ENGLISH)
            .values_list("id", flat=True)
        )

        progress_qs = (
            ge_models.UserProgress.objects
            .filter(user=obj, course_id__in=ge_course_ids)
            .select_related("course")
        )

        return ge_serializers.UserProgressSerializer(progress_qs, many=True).data


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
