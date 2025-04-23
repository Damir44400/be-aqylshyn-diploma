from rest_framework import serializers

from apps.ielts import models
from .listening_question import IeltsListeningQuestionSerializer


class IeltsListeningPartSerializer(serializers.ModelSerializer):
    questions = IeltsListeningQuestionSerializer(
        many=True, read_only=True
    )

    part_label = serializers.CharField(
        source="get_part_display", read_only=True
    )

    class Meta:
        model = models.IeltsListeningPart
        fields = (
            "id",
            "part",
            "part_label",
            "questions",
        )
        read_only_fields = fields
