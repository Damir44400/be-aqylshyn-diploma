from rest_framework_json_api import serializers


class IeltsListeningOptionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    option = serializers.CharField(read_only=True)
