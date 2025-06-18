import json
from typing import Tuple

from pydantic import ValidationError

from apps.ai_chat import models
from apps.ai_chat.models import ChatMessage, ChatFile
from apps.common import enums
from apps.llms import openai_cli
from apps.llms.prompts.ai_chat_prompt import get_ai_chat_prompt
from apps.llms.tasks import parse_json_response


class ChatService:
    SYSTEM_PROMPT = get_ai_chat_prompt()

    def send_message(self, data: dict, user) -> Tuple[str, int]:
        chat_id = data.get('chat_id')
        message = data['message']
        file = data.get('file')
        if not file:
            file = ChatFile.objects.filter(chat_id=chat_id).last()
            if file:
                file = file.file
        client = openai_cli.OpenAICLI()
        chat_history = models.ChatMessage.objects.filter(
            chat_id=chat_id
        ).order_by(
            "-created_at"
        )[:5]
        system_prompt = self.SYSTEM_PROMPT
        try:
            response = client.send_request(
                system_prompt,
                data=message,
                chat_history=chat_history,
                file=file,
            )
            json_response = parse_json_response(response)
        except (json.JSONDecodeError, KeyError) as exc:
            raise ValidationError(
                "Не удалось обработать ответ модели. Попробуйте ещё раз."
            ) from exc

        db_chat = models.Chats.objects.filter(id=chat_id).first()
        if not db_chat:
            name = json_response.get("name", "Новый чат")
            db_chat = models.Chats.objects.create(name=name, user=user)

        ChatMessage.objects.create(
            chat_id=db_chat.pk,
            text=message,
            sender=enums.ChatSenderType.USER,
        )
        ChatMessage.objects.create(
            chat_id=db_chat.pk,
            text=json_response.get("answer", ""),
            sender=enums.ChatSenderType.AI,
        )
        ChatFile.objects.create(
            chat_id=db_chat.pk,
            file=file
        )
        return json_response.get("answer", ""), db_chat.pk
