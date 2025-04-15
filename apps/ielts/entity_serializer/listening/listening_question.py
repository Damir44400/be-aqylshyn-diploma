from rest_framework import serializers

from apps.common import enums
from apps.general_english.entity_serializers.listenings.listening_option import ListeningOptionSerializer
from apps.ielts import models


class IeltsListeningQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    
    class Meta:
        model = models.IeltsListeningQuestion
        fields = (
            "id",
            "question_content",
            "question_type",
            "options",
        )


    def get_options(self, obj):
        if obj.question_type == enums.IeltsListeningQuestionType.OPTIONS:
            return ListeningOptionSerializer(obj.options.all(), many=True).data
        return []
