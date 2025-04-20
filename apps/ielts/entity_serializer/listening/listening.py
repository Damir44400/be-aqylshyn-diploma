from rest_framework import serializers

from apps.ielts import models
from .listening_question import IeltsListeningQuestionSerializer


class IeltsListeningSerializer(serializers.ModelSerializer):
    questions = IeltsListeningQuestionSerializer(
        many=True, read_only=True
    )

    part_label = serializers.CharField(
        source="get_part_display", read_only=True
    )

    class Meta:
        model = models.IeltsListening
        fields = (
            "id",
            "part",
            "part_label",
            "title",
            "audio_file",
            "questions",
        )
        read_only_fields = fields
