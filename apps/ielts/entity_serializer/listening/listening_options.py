from rest_framework_json_api import serializers

from apps.ielts import models


class IeltsListeningOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IeltsListeningOption
        fields = (
            "id",
            "option"
        )
