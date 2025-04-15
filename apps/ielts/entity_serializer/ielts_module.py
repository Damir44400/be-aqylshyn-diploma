from rest_framework import serializers

from apps.ielts import models
from apps.ielts.entity_serializer.ielts_sub_module import IeltsSubModuleDetailSerializer


class IeltsModuleSerializer(serializers.ModelSerializer):
    sub_modules = IeltsSubModuleDetailSerializer(many=True, read_only=True)

    class Meta:
        model = models.IeltsModule
        fields = (
            "id",
            "title",
            "cover",
            "sub_modules",
        )
