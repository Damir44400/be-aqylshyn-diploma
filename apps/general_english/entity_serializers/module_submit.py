from rest_framework import serializers


class OptionSubmitSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    question_id = serializers.IntegerField()


class ModuleOptionSubmitSerializer(serializers.Serializer):
    options = OptionSubmitSerializer(many=True)


class WritingSubmitSerializer(serializers.Serializer):
    text = serializers.CharField()


class ModuleWritingSubmitSerializer(serializers.Serializer):
    writing = WritingSubmitSerializer(many=False)


class SpeakingSubmitSerializer(serializers.Serializer):
    speaking_id = serializers.IntegerField()
    text = serializers.CharField()


class ModuleSpeakingSubmitSerializer(serializers.Serializer):
    speaking = SpeakingSubmitSerializer(many=True)
