from rest_framework import serializers

from apps.general_english import models


class ReadingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReadingOption
        fields = (
            'id',
            'option',
        )
