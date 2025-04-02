from rest_framework import serializers

from apps.ielts import models
from .ielts_sub_module import IeltsSubModuleSerializer

class IeltsModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IeltsModule
        fields = (
            "id",
            "title",
            "cover",
        )


class IeltsModuleDetailSerializer(IeltsModuleSerializer):
    sub_modules = IeltsSubModuleSerializer(many=True, read_only=True)

    class Meta(IeltsModuleSerializer.Meta):
        fields = IeltsModuleSerializer.Meta.fields + (
            "sub_modules",
        )
