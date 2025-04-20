from rest_framework import serializers

from apps.ielts import models


class IeltsSpeakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IeltsSpeakingQuestion
        fields = (
            "id",
            "question",
            "additional_information",
        )