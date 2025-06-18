from rest_framework import serializers

from apps.ai_chat import models


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chats
        fields = (
            'id',
            'name'
        )


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = models.ChatMessage
        fields = (
            "id",
            "text",
            "sender",
            "sender_name"
        )

    def get_sender_name(self, obj):
        if obj.sender == "USER":
            return obj.chat.user.first_name
        else:
            return "AQYLBEK"


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Chats
        fields = (
            "id",
            "name",
            "messages"
        )


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
    chat_id = serializers.IntegerField(required=False)
    file = serializers.FileField(required=False)
