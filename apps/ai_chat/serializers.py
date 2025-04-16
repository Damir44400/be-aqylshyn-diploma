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
    class Meta:
        model = models.ChatMessage
        fields = (
            "id",
            "text",
            "sender"
        )


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
