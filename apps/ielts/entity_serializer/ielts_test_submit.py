from rest_framework import serializers


class IeltsWritingSubmit(serializers.Serializer):
    answer = serializers.CharField()
    writing_id = serializers.IntegerField()


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
