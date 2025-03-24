from rest_framework import serializers


class OptionSubmitSerializer(serializers.Serializer):
    option_id = serializers.IntegerField()
    question_id = serializers.IntegerField()


class ModuleOptionSubmitSerializer(serializers.Serializer):
    section_name = serializers.ChoiceField(choices=[("reading", "reading"), ("listening", "listening")])
    options = OptionSubmitSerializer(many=True)


class TextSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    text = serializers.CharField()


class ModuleAnswerSubmitSerializer(serializers.Serializer):
    section_name = serializers.ChoiceField(choices=[("speaking", "speaking"), ("writing", "writing")])
    answers = TextSubmitSerializer(many=True)
