from drf_spectacular.extensions import OpenApiSerializerExtension
from rest_framework import serializers

from apps.ielts import models as ielts_models
from . import ielts_writing
from .listening import listening
from .readings import reading


class IeltsTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ielts_models.IeltsTest
        fields = (
            "id",
            "name"
        )
OpenApiSerializerExtension

class IeltsTestDetailSerializer(IeltsTestSerializer):
    readings = reading.IeltsReadingSerializer(many=True)
    listenings = listening.IeltsListeningSerializer(many=True)
    writings = ielts_writing.IeltsWritingSerializer(many=True)

    class Meta(IeltsTestSerializer.Meta):
        fields = IeltsTestSerializer.Meta.fields + (
            "readings",
            "listenings",
            "writings",
        )
