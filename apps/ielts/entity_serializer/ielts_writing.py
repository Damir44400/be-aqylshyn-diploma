from rest_framework import serializers

from apps.ielts import models


class IeltsWritingImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WritingImage
        fields = (
            "id",
            "image",
        )


class IeltsWritingSerializer(serializers.ModelSerializer):
    images = IeltsWritingImagesSerializer(many=True, read_only=True)
    is_passed = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = models.IeltsWriting
        fields = (
            "id",
            "title",
            "description",
            "images",
            "is_passed",
            "score",
        )

    def get_is_passed(self, obj):
        user = self.context.get("request").user
        test_submit = models.IeltsTestSubmit.objects.filter(test=obj.test, section="WRITING", user=user).first()
        if test_submit:
            return True
        return False

    def get_score(self, obj):
        user = self.context.get("request").user
        test_submit = models.IeltsTestSubmit.objects.filter(test=obj.test, section="WRITING", user=user).first()
        if test_submit:
            return test_submit.score
        return -1
