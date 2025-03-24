from rest_framework import serializers

from apps.general_english import models


class ListeningOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ListeningOption
        fields = (
            'id',
            'option'
        )
