from rest_framework import serializers

from apps.general_english import models
from .listenings.listening_question import ListeningQuestionSerializer
from .readings.reading_question import ReadingQuestionSerializer
from .speaking import SpeakingSerializer
from .writing import WritingSerializer
from ...common import enums


class ModuleSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()

    class Meta:
        model = models.Module
        fields = (
            'id',
            'name',
            'is_completed',
            'total_score',
            'sections',
        )

    def get_score(self, obj, section_type):
        score_obj = models.ModuleScore.objects.filter(
            module=obj,
            section=getattr(enums.ModuleSectionType, section_type.upper())
        ).first()
        return score_obj.score if score_obj else None

    def get_sections(self, obj):
        sections = {}
        for section in ['writing', 'reading', 'listening', 'speaking']:
            has_field = getattr(obj, f'has_{section}')
            score = self.get_score(obj, section) if has_field else None
            sections[section] = {
                'has_section': has_field,
                'already_passed': score is not None and score > 0,
                'score': score,
            }
        return sections

    def get_total_score(self, obj):
        total = 0
        for section in ['writing', 'reading', 'listening', 'speaking']:
            has_field = getattr(obj, f'has_{section}')
            score = self.get_score(obj, section) if has_field else 0
            total += score or 0
        return total


class ModuleReadingSerializer(serializers.ModelSerializer):
    readings = ReadingQuestionSerializer(many=True)

    class Meta:
        model = models.Module
        fields = (
            'id',
            'name',
            'readings',
        )


class ModuleWritingSerializer(serializers.ModelSerializer):
    writing = serializers.SerializerMethodField()

    class Meta:
        model = models.Module
        fields = (
            "id",
            "name",
            "writing",
        )

    def get_writing(self, obj):
        return models.Writing.objects.filter(module=obj).first()


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
