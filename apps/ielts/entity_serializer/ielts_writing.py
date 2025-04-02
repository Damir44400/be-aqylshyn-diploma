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

    class Meta:
        model = models.IeltsWriting
        fields = (
            "id",
            "title",
            "description",
            "images",
        )
