from rest_framework import serializers

from apps.ielts import models as ielts_models
from . import ielts_writing
from .listening import listening
from .readings import reading
from .speakings import ielts_speaking_parts
from ...common import enums


class IeltsTestSerializer(serializers.ModelSerializer):
    passed_sections = serializers.SerializerMethodField()

    class Meta:
        model = ielts_models.IeltsTest
        fields = (
            "id",
            "name",
            "passed_sections",
        )

    def get_passed_sections(self, obj):
        user = self.context.get("request").user
        sections = [
            enums.ModuleSectionType.LISTENING,
            enums.ModuleSectionType.READING,
            enums.ModuleSectionType.WRITING,
            enums.ModuleSectionType.SPEAKING
        ]
        payload = []
        for section in sections:
            section_score = ielts_models.IeltsTestSubmit.objects.filter(
                test=obj,
                section=section,
                user=user,
            ).only("score").first()
            if section_score:
                payload.append(
                    {
                        "section": section,
                        "is_passed": True,
                        "score": section_score.score,
                    }
                )
            else:
                payload.append(
                    {
                        "section": section,
                        "is_passed": False,
                        "score": None,
                    }
                )
        return payload


class IeltsTestDetailSerializer(IeltsTestSerializer):
    reading_passages = reading.IeltsReadingSerializer(many=True)
    listening_part = listening.IeltsListeningSerializer(many=False)
    writing_tasks = ielts_writing.IeltsWritingSerializer(many=True)
    speaking_parts = ielts_speaking_parts.IeltsSpeakingPartsSerializer(many=True)

    class Meta(IeltsTestSerializer.Meta):
        fields = IeltsTestSerializer.Meta.fields + (
            "reading_passages",
            "listening_part",
            "writing_tasks",
            "speaking_parts",
        )
