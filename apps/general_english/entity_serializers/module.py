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
            "order",
            'sections',
        )

    def get_sections(self, obj):
        """
        Возвращает структуру вида:
        {
            "writing": {
                "has_section": True/False,
                "already_passed": True/False,
                "score": 10,
                "max_score": 25,
            },
            ...
        }
        """
        scores_map = {
            score_obj.section: score_obj.score
            for score_obj in obj.modulescore_set.all()
        }

        sections_data = {}
        for section in ['writing', 'reading', 'listening', 'speaking']:
            has_section = getattr(obj, f'has_{section}', False)
            if has_section:
                enum_val = getattr(enums.ModuleSectionType, section.upper())
                user_score = scores_map.get(enum_val, None)
                max_score = self.get_section_question_count(obj, section)
            else:
                user_score = None
                max_score = None

            sections_data[section] = {
                'has_section': has_section,
                'already_passed': user_score is not None,
                'score': user_score,
                'max_score': max_score,
            }

        return sections_data

    def get_total_score(self, obj):
        scores_map = {
            score_obj.section: score_obj.score
            for score_obj in obj.modulescore_set.all()
        }

        total_score_value = 0

        for section in ['writing', 'reading', 'listening', 'speaking']:
            if getattr(obj, f'has_{section}', False):
                enum_val = getattr(enums.ModuleSectionType, section.upper())
                user_score = scores_map.get(enum_val, 0)
                total_score_value += user_score

        return {
            'score': total_score_value,
            'max_score': self.get_section_question_count(obj, section)
        }

    def get_section_question_count(self, obj, section):
        if section == 'reading':
            return obj.readings.count()
        elif section == 'listening':
            return obj.listening_questions.count()
        elif section == 'speaking':
            return obj.speakings.count()
        elif section == 'writing':
            return 1
        return 0


class ModuleReadingSerializer(serializers.ModelSerializer):
    readings = ReadingQuestionSerializer(many=True)
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = models.Module
        fields = (
            'id',
            'name',
            'readings',
            'total_questions',
        )

    def get_total_questions(self, obj):
        return obj.readings.count()


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
        instance = models.Writing.objects.filter(module=obj).first()
        if instance:
            return WritingSerializer(instance, many=False).data
        return {}


class ModuleListeningSerializer(serializers.ModelSerializer):
    listening_questions = ListeningQuestionSerializer(many=True)
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = models.Module
        fields = (
            "id",
            "name",
            "listening_questions",
            "total_questions",
        )

    def get_total_questions(self, obj):
        return obj.listening_questions.count()


class ModuleSpeakingSerializer(serializers.ModelSerializer):
    speakings = SpeakingSerializer(many=True)
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = models.Module
        fields = (
            "id",
            "name",
            "speakings",
            "total_questions",
        )

    def get_total_questions(self, obj):
        return obj.speakings.count()
