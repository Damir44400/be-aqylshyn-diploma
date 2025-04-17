import json
from typing import Tuple

from pydantic_core import ValidationError

from apps.ai_chat import models
from apps.ai_chat.models import ChatMessage
from apps.common import enums
from apps.llms import openai_cli
from apps.llms.prompts.ai_chat_prompt import get_ai_chat_prompt


class ChatService:
    def send_message(self, data, user) -> Tuple[str, int]:
        chat_id = data['chat_id']
        message = data['message']
        db_chat = models.Chats.objects.filter(id=chat_id).first()
        client = openai_cli.OpenAICLI()

        try:
            response = client.send_request(get_ai_chat_prompt(), data=message)
            json_response = json.loads(response)
        except (json.JSONDecodeError, KeyError):
            raise ValidationError("Произошла ошибка при обработке ответа. Пожалуйста, повторите попытку.")

        if not db_chat:
            name = json_response.get("name", "Новый чат")
            db_chat = models.Chats.objects.create(name=name, user=user)

        ChatMessage.objects.create(
            chat_id=db_chat.pk,
            text=message,
            sender=enums.ChatSenderType.USER
        )

        ChatMessage.objects.create(
            chat_id=db_chat.pk,
            text=json_response.get("answer", ""),
            sender=enums.ChatSenderType.AI
        )

        return json_response.get("answer", ""), db_chat.pk
