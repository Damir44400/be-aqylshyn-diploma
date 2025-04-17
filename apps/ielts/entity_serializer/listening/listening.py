from rest_framework import serializers

from apps.ielts import models
from .listening_question import IeltsListeningQuestionSerializer


class IeltsListeningSerializer(serializers.ModelSerializer):
    questions = IeltsListeningQuestionSerializer(many=True, read_only=True)
    is_passed = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = models.IeltsListening
        fields = ("id", "title", "audio_file", "is_passed", "score", "questions")

    def get_is_passed(self, obj):
        user = self.context.get("request").user
        test_submit = models.IeltsTestSubmit.objects.filter(test=obj.test, section="LISTENING", user=user).first()
        if test_submit:
            return True
        return False

    def get_score(self, obj):
        user = self.context.get("request").user
        test_submit = models.IeltsTestSubmit.objects.filter(test=obj.test, section="LISTENING", user=user).first()
        if test_submit:
            return test_submit.score
        return -1
