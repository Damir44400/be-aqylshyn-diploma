from rest_framework import serializers

from apps.general_english import models as general_english_models


class TrialOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = general_english_models.TrialOption
        fields = (
            'id',
            'option',
        )
