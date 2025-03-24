from rest_framework import serializers

from apps.general_english import models as general_english_models
from .trial_option import TrialOptionSerializer


class TrialQuestionSerializer(serializers.ModelSerializer):
    options = TrialOptionSerializer(many=True, read_only=True, source="trial_options")

    class Meta:
        model = general_english_models.TrialQuestion
        fields = [
            'id',
            'question',
            'question_type',
            'options',
        ]
