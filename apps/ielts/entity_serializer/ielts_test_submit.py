from rest_framework import serializers


class _WritingSubmit(serializers.Serializer):
    answer = serializers.CharField()
    writing_id = serializers.IntegerField()


class _SpeakingSubmit(serializers.Serializer):
    answer = serializers.CharField()
    speaking_id = serializers.IntegerField()


class IeltsWritingSubmit(serializers.Serializer):
    writings = _WritingSubmit(many=True)


class IeltsSpeakingSubmit(serializers.Serializer):
    speakings = _SpeakingSubmit(many=True)


class IeltsOptionsSubmit(serializers.Serializer):
    option_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    section = serializers.ChoiceField(
        choices=(
            ("LISTENING", "LISTENING"),
            ("READING", "READING"),
        )
    )


class IeltsFillBlankSubmit(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.ListField(
        child=serializers.CharField()
    )
    section = serializers.ChoiceField(
        choices=(
            ("LISTENING", "LISTENING"),
            ("READING", "READING"),
        )
    )


class IeltsSelectInsertSubmit(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()
