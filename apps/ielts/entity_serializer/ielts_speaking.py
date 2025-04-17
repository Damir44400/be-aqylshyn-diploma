from rest_framework import serializers

from apps.ielts import models


class IeltsSpeakingSerializer(serializers.ModelSerializer):
    is_passed = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = models.IeltsSpeakingQuestion
        fields = (
            "id",
            "question",
            "additional_information",
            "is_passed",
            "score",
        )

    def get_is_passed(self, obj):
        user = self.context.get("request").user
        test_submit = models.IeltsTestSubmit.objects.filter(test=obj.test, section="SPEAKING", user=user).first()
        if test_submit:
            return True
        return False

    def get_score(self, obj):
        user = self.context.get("request").user
        test_submit = models.IeltsTestSubmit.objects.filter(test=obj.test, section="SPEAKING", user=user).first()
        if test_submit:
            return test_submit.score
        return -1
