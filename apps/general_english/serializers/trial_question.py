from rest_framework import serializers

from apps.general_english import models as general_english_models
from apps.general_english import serializers as general_english_serializers


class TrialQuestionSerializer(serializers.ModelSerializer):
    options = general_english_serializers.TrialOptionSerializer(many=True)

    class Meta:
        model = general_english_models.TrialQuestion
        fields = [
            'id',
            'question',
            'question_type',
            'options',
        ]

    def get_options(self, obj):
        return obj.trial_options.all()
