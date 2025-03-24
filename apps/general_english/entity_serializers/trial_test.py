from django.core import validators
from rest_framework import serializers


class TrialQuestionPassSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(required=True, validators=[validators.MinValueValidator(1)])
    option_id = serializers.IntegerField(required=False)
    text_answer = serializers.CharField(required=False, allow_blank=False)

    def validate(self, attrs):
        if "text_answer" in attrs and not attrs["text_answer"].strip():
            raise serializers.ValidationError("Text answer cannot be empty")

        if "option_id" in attrs and attrs["option_id"] <= 0:
            raise serializers.ValidationError("Option id must be positive")

        return attrs


class TrialTestSerializer(serializers.Serializer):
    answers = TrialQuestionPassSerializer(many=True)
