from rest_framework import serializers

from apps.general_english import models as general_english_models


class CourseSerializer(serializers.ModelSerializer):
    user_progress = serializers.SerializerMethodField()
    modules_count = serializers.SerializerMethodField()

    class Meta:
        model = general_english_models.Course
        fields = (
            'id',
            'name',
            "modules_count",
            "for_level",
            'has_level_define',
        )

    def get_modules_count(self, obj):
        if hasattr(obj, 'user_courses'):
            return obj.user_courses.get_modules_count()
        else:
            return None

    def get_user_progress(self, obj):
        if hasattr(obj, 'user_courses'):
            return obj.user_courses.get_progress()
        else:
            return None

class CourseRetrieveSerializer(serializers.ModelSerializer):
    class Meta(CourseSerializer.Meta):
        model = general_english_models.Course
        fields = [
            "description",
            "duration",
            "last_module"
        ]