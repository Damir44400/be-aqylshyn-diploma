from rest_framework import serializers

from apps.ielts import models
from apps.ielts.entity_serializer.speakings.ielts_speaking_questions import IeltsSpeakingSerializer


class IeltsSpeakingPartsSerializer(serializers.ModelSerializer):
    speaking_questions = IeltsSpeakingSerializer(many=True, read_only=True)

    class Meta:
        model = models.IeltsSpeakingPart
        fields = (
            "part",
            "speaking_questions"
        )
