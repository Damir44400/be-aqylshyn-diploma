from rest_framework import serializers

from apps.ielts import models


class IeltsListeningQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IeltsListeningQuestion
        fields = (
            "id",
            "question_content",
            "question_type",
        )
