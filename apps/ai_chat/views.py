from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.ai_chat import services
from apps.ai_chat.models import Chats
from apps.ai_chat.serializers import ChatSerializer, MessageSerializer, ChatDetailSerializer
from apps.common import mixins as common_mixins


class ChatViewSet(common_mixins.ActionSerializerMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializers = {
        "chats": ChatSerializer,
        "send_message": MessageSerializer,
        "chat_history": ChatDetailSerializer,
    }
    service = services.ChatService()

    @action(detail=False, methods=["get"], url_path="")
    def chats(self, request):
        queryset = Chats.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="messages")
    def send_message(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = self.service.send_message(serializer.validated_data, user=request.user)
        return Response({"answer": answer}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="history")
    def chat_history(self, request, pk=None):
        queryset = Chats.objects.filter(user=request.user,id=pk).first()
        if not queryset:
            raise ValidationError("Chat not found")
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)
