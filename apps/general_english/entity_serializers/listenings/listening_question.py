from rest_framework import serializers

from apps.general_english import models
from .listening_option import ListeningOptionSerializer


class ListeningQuestionSerializer(serializers.ModelSerializer):
    options = ListeningOptionSerializer(many=True, read_only=True)

    class Meta:
        model = models.ListeningQuestion
        fields = (
            'id',
            'audio_question',
            'context',
            'options',
        )
