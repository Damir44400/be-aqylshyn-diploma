from rest_framework import serializers


class ReadingOptionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    option = serializers.CharField()
    is_correct = serializers.BooleanField()


class ReadingSelectInsertSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    options = serializers.JSONField()
