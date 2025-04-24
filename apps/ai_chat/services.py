import io
import json
import os
from contextlib import suppress
from typing import Generator, List, Tuple

import chardet
import pdfplumber
from django.utils.text import Truncator
from docx import Document
from pydantic import ValidationError

from apps.ai_chat import models
from apps.ai_chat.models import ChatMessage
from apps.common import enums
from apps.llms import openai_cli
from apps.llms.prompts.ai_chat_prompt import get_ai_chat_prompt


class ChatService:
    SYSTEM_PROMPT = get_ai_chat_prompt()

    HEAVY_FILE_BYTES = 100 * 1024  # ≥100 KB считаем «тяжёлым»
    CHUNK_SIZE = 3_000  # берём ~3 тыс. симв. на чанк
    SUMMARY_TOKENS = 300  # просим модель ужать до ≈300 токенов

    def _chunk_stream(self, stream: io.BufferedReader) -> Generator[str, None, None]:
        while True:
            piece = stream.read(self.CHUNK_SIZE)
            if not piece:
                break
            yield piece

    def _summarize(self, text: str, client: openai_cli.OpenAICLI) -> str:
        prompt = (
            "Прочти фрагмент текста и сделай краткий конспект "
            f"примерно в {self.SUMMARY_TOKENS} токенов:\n\n{text}"
        )
        with suppress(Exception):
            response = client.send_request(prompt, data={})
            return response.strip()
        return Truncator(text).chars(self.SUMMARY_TOKENS * 4, truncate=" …")

    def send_message(self, data, user) -> Tuple[str, int]:
        chat_id = data.get('chat_id')
        message = data['message']
        files = data.get('files', [])

        client = openai_cli.OpenAICLI()
        chat_message = models.ChatMessage.objects.filter(chat_id=chat_id).order_by("-created_at")[:10]
        context_fragments = self._extract_text_context(files, client)
        system_prompt = self.SYSTEM_PROMPT
        try:
            response = client.send_request(
                system_prompt,
                data=message,
                chat_message=chat_message,
                context_fragments=context_fragments,
            )
            json_response = json.loads(response)
        except (json.JSONDecodeError, ValidationError, KeyError) as exc:
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

        return json_response.get("answer", ""), db_chat.pk

    def _extract_text_context(self, files: List[io.BufferedReader], client: openai_cli.OpenAICLI) -> List[str]:
        context = []

        for file in files:
            filename = file.name
            ext = os.path.splitext(filename)[1].lower()

            text = ""
            if ext == ".txt":
                text = self._extract_txt(file)
            elif ext == ".docx":
                text = self._extract_docx(file)
            elif ext == ".pdf":
                text = self._extract_pdf(file)

            if not text:
                continue

            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            if file_size >= self.HEAVY_FILE_BYTES:
                text = self._summarize(text, client)

            context.append(f"[Файл: {filename}]\n{text}")

        return context

    def _extract_txt(self, file: io.BufferedReader) -> str:
        raw = file.read()
        encoding = chardet.detect(raw)['encoding']
        return raw.decode(encoding or 'utf-8', errors='ignore')

    def _extract_docx(self, file: io.BufferedReader) -> str:
        doc = Document(file)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    def _extract_pdf(self, file: io.BufferedReader) -> str:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
