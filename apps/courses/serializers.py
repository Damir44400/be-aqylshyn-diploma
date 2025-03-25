from rest_framework import serializers

from apps.courses import models as courses_models


class CourseSerializer(serializers.ModelSerializer):
    modules_count = serializers.SerializerMethodField()
    trial_passed = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = courses_models.Course
        fields = (
            'id',
            'name',
            "modules_count",
            'has_level_define',
            "trial_passed",
            "user_progress",
        )

    def get_modules_count(self, obj):
        user = self.context['request'].user
        if hasattr(obj, 'user_course'):
            user_course = obj.user_course.filter(user=user).first()
            return user_course.get_modules_count if user_course else 0
        return None

    def get_trial_passed(self, obj):
        user = self.context['request'].user
        if hasattr(obj, 'user_course'):
            return obj.user_course.filter(user=user).exists()
        return False

    def get_user_progress(self, obj):
        user = self.context['request'].user
        if hasattr(obj, 'user_course'):
            user_course = obj.user_course.filter(user=user).first()
            return user_course.get_progress if user_course else 0
        return None
