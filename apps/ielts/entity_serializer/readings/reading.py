from rest_framework import serializers

from apps.ielts import models
from .reading_question import ReadingQuestionSerializer


class IeltsReadingSerializer(serializers.ModelSerializer):
    questions = ReadingQuestionSerializer(many=True, read_only=True)
    is_passed = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = models.IeltsReading
        fields = (
            "id",
            "title",
            "content",
            "questions",
            "is_passed",
            "score",
        )

    def get_is_passed(self, obj):
        user = self.context.get("request").user
        test_submit = models.IeltsTestSubmit.objects.filter(test=obj.test, section="READING", user=user).first()
        if test_submit:
            return True
        return False

    def get_score(self, obj):
        user = self.context.get("request").user
        test_submit = models.IeltsTestSubmit.objects.filter(test=obj.test, section="READING", user=user).first()
        if test_submit:
            return test_submit.score
        return -1
