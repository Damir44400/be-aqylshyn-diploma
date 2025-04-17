from rest_framework import serializers

from apps.ielts import models as ielts_models
from . import ielts_writing, ielts_speaking
from .listening import listening
from .readings import reading


class IeltsTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ielts_models.IeltsTest
        fields = (
            "id",
            "name"
        )


class IeltsTestDetailSerializer(IeltsTestSerializer):
    readings = reading.IeltsReadingSerializer(many=True)
    listenings = listening.IeltsListeningSerializer(many=True)
    writings = ielts_writing.IeltsWritingSerializer(many=True)
    speakings = ielts_speaking.IeltsSpeakingSerializer(many=True)

    class Meta(IeltsTestSerializer.Meta):
        fields = IeltsTestSerializer.Meta.fields + (
            "readings",
            "listenings",
            "writings",
            "speakings",
        )
