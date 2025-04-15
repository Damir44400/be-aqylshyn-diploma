from rest_framework import serializers


class ReadingOptionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    option = serializers.CharField()


class ReadingSelectInsertSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    options = serializers.JSONField()
