from apps.ai_chat import models
from apps.llms import openai_cli
class ChatService:
    def send_message(self, message: str, chat_id: int, user):
        db_chat = models.Chats.objects.filter(id=chat_id).first()
        client = openai_cli.OpenAICLI()
        if not db_chat:
            response = client.send_request()
            db_chat = models.Chats.objects.create()
