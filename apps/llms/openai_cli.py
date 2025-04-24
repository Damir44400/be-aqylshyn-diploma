import openai
from django.conf import settings


class OpenAICLI:
    def __init__(self):
        self.openai_cli = openai.OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def send_request(self, system_prompt, **kwargs):
        try:
            user_data = kwargs.get("data", "")
            chat_message = kwargs.get("chat_message", "")
            context_fragments = kwargs.get("context_fragments", "")
            if not isinstance(user_data, str):
                user_data = str(user_data)

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_data},
            ]

            for context in context_fragments:
                messages.append({"role": "user", "content": f"File context: {context}"})

            if chat_message:
                for chat in chat_message:
                    role = "user"
                    if chat.sender == "AI":
                        role = "system"
                    messages.append(
                        {
                            "role": role,
                            "content": chat.text
                        }
                    )

            response = self.openai_cli.chat.completions.create(
                model='gpt-4o-mini-2024-07-18',
                messages=messages
            )

            llm_response = response.choices[0].message.content
            if isinstance(llm_response, bytes):
                llm_response = llm_response.decode('utf-8')

            return llm_response

        except Exception as e:
            return {"error": "An unexpected error occurred while processing the AI response."}
