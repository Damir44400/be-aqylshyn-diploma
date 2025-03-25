from rest_framework import serializers

from apps.general_english import models as general_english_models


class UserProgressSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    last_module_name = serializers.SerializerMethodField()
    progress_percentage = serializers.ReadOnlyField(source="get_progress")
    modules_count = serializers.ReadOnlyField(source="get_modules_count")

    class Meta:
        model = general_english_models.UserProgress
        fields = [
            'course_id',
            'course_name',
            "last_module",
            "last_module_name",
            "progress_percentage",
            "modules_count"
        ]

    def get_course_name(self, obj):
        return obj.course.name

    def get_last_module_name(self, obj):
        if obj.last_module:
            return obj.last_module.name
        return None
