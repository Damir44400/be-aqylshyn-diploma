from rest_framework import serializers

from apps.ielts import models
from .listening_parts import IeltsListeningPartSerializer


class IeltsListeningSerializer(serializers.ModelSerializer):
    listening_parts = IeltsListeningPartSerializer(many=True)

    class Meta:
        model = models.IeltsListening
        fields = (
            "id",
            "title",
            "audio_file",
            'listening_parts',
        )
        read_only_fields = fields
