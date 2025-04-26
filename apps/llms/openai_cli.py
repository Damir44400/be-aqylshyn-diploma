import openai
from django.conf import settings


class OpenAICLI:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def send_request(self, system_prompt: str, **kwargs):
        try:
            user_data = kwargs.get("data", "")
            chat_messages = kwargs.get("chat_message", [])
            context_fragments = kwargs.get("context_fragments", [])
            model = kwargs.get("model", "gpt-4o-mini-2024-07-18")
            messages = [
                {"role": "system", "content": system_prompt},
            ]

            if user_data:
                if not isinstance(user_data, str):
                    user_data = str(user_data)
                messages.append({"role": "user", "content": user_data})

            for context in context_fragments:
                messages.append({"role": "user", "content": f"File context: {context}"})

            for chat in chat_messages:
                role = "system" if getattr(chat, "sender", "user") == "AI" else "user"
                messages.append({"role": role, "content": getattr(chat, "text", "")})

            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )

            content = response.choices[0].message.content
            return content.decode('utf-8') if isinstance(content, bytes) else content

        except Exception as e:
            return {"error": "An unexpected error occurred while processing the AI response."}
