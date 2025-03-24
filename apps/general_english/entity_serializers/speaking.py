from rest_framework import serializers

from apps.general_english import models


class SpeakingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Speaking
        fields = (
            'context',
        )
