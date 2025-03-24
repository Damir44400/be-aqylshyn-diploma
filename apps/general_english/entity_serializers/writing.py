from rest_framework import serializers

from apps.general_english import models


class WritingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Writing
        fields = (
            'id',
            'title',
            'requirements',
        )
