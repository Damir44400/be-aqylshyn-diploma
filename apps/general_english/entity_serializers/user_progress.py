from rest_framework import serializers

from apps.general_english import models as general_english_models


class UserProgressSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.ReadOnlyField(source="get_progress")
    modules_count = serializers.ReadOnlyField(source="get_modules_count")

    class Meta:
        model = general_english_models.UserProgress
        fields = [
            "course",
            "score",
            "last_module",
            "progress_percentage",
            "modules_count"
        ]
