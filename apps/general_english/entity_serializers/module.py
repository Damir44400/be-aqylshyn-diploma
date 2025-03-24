from rest_framework import serializers

from apps.general_english import models
from .listenings.listening_question import ListeningQuestionSerializer
from .readings.reading import ReadingSerializer
from .speaking import SpeakingSerializer
from .writing import WritingSerializer


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = (
            'id',
            'name',
            'is_completed',
            'has_writing',
            'has_reading',
            'has_listening',
            'has_speaking',
        )


class ModuleReadingSerializer(serializers.ModelSerializer):
    reading = ReadingSerializer(many=False)

    class Meta:
        model = models.Module
        fields = (
            'id',
            'name',
            'reading',
        )


class ModuleWritingSerializer(serializers.ModelSerializer):
    writing = WritingSerializer(many=True)

    class Meta:
        model = models.Module
        fields = (
            "id",
            "name",
            "writing",
        )


class ModuleListeningSerializer(serializers.ModelSerializer):
    listening_questions = ListeningQuestionSerializer(many=True)

    class Meta:
        model = models.Module
        fields = (
            "id",
            "name",
            "listening_questions",
        )

class ModuleSpeakingSerializer(serializers.ModelSerializer):
    speakings = SpeakingSerializer(many=True)
    class Meta:
        model = models.Module
        fields = (
            "id",
            "name",
            "speakings",
        )