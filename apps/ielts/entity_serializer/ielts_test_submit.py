from rest_framework import serializers


class _WritingSubmit(serializers.Serializer):
    answer = serializers.CharField()
    writing_id = serializers.IntegerField()


class _SpeakingSubmit(serializers.Serializer):
    answer = serializers.CharField()
    speaking_id = serializers.IntegerField()


class _OptionsSubmit(serializers.Serializer):
    option_id = serializers.IntegerField()
    question_id = serializers.IntegerField()


class _FillBlankSubmit(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.ListField(
        child=serializers.CharField()
    )


class _SelectInsertSubmit(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()


class _ListeningSubmit(serializers.Serializer):
    options = _OptionsSubmit(many=True)
    fills = _FillBlankSubmit(many=True)
    listening_id = serializers.IntegerField()


class _ReadingSubmit(serializers.Serializer):
    options = _OptionsSubmit(many=True)
    fills = _FillBlankSubmit(many=True)
    selects = _SelectInsertSubmit(many=True)
    reading_id = serializers.IntegerField()


class IeltsWritingSubmit(serializers.Serializer):
    writings = _WritingSubmit(many=True)


class IeltsSpeakingSubmit(serializers.Serializer):
    speakings = _SpeakingSubmit(many=True)


class IeltsReadingSubmit(serializers.Serializer):
    readings = _ReadingSubmit(many=True)


class IeltsListeningSubmit(serializers.Serializer):
    listening = _ListeningSubmit(many=False)
