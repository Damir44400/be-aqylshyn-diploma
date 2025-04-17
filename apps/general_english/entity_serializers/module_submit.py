from rest_framework import serializers


class OptionSubmitSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    question_id = serializers.IntegerField()


class ModuleOptionSubmitSerializer(serializers.Serializer):
    options = OptionSubmitSerializer(many=True)


class ModuleWritingSubmitSerializer(serializers.Serializer):
    writing = serializers.CharField()


class SpeakingSubmitSerializer(serializers.Serializer):
    speaking_id = serializers.IntegerField()
    text = serializers.CharField()


class ModuleSpeakingSubmitSerializer(serializers.Serializer):
    answers = SpeakingSubmitSerializer(many=True)


class ModuleScoreSerializer(serializers.Serializer):
    section = serializers.CharField()
    score = serializers.IntegerField()


class OptionAttemptSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    question_id = serializers.IntegerField()


class WritingAttemptSerializer(serializers.Serializer):
    writing = serializers.CharField()
    ai_response = serializers.CharField()
