from rest_framework import serializers

from apps.ielts import models


class ReadingOptionsSerializer(serializers.Serializer):
    class Meta:
        model = models.IeltsReadingOption
        fields = (
            "id",
            "option"
        )


class ReadingSelectInsertSerializer(serializers.Serializer):
    class Meta:
        model = models.IeltsReadingSelectInsert
        fields = (
            "id",
            "options"
        )
