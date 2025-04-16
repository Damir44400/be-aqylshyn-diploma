from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from apps.ai_chat.serializers import ChatSerializer, ChatMessageSerializer
from apps.common import mixins as common_mixins


# Create your views here.
class ChatViewSet(
    common_mixins.ActionSerializerMixin,
    viewsets.GenericViewSet
):
    permission_classes = (permissions.IsAuthenticated,)
    serializers = {
        "chats": ChatSerializer,
        "messages": ChatMessageSerializer,
    }

    @action(detail=False, methods=["post"], url_path="<chat_id: int>/messages")
    def messages(self, request, chat_id=None):
