import base64
import mimetypes
import os
import tiktoken

import openai
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import FieldFile

from apps.common import enums


class OpenAICLI:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.max_tokens = 120000

    def _get_encoding(self, model: str):
        try:
            return tiktoken.encoding_for_model(model)
        except KeyError:
            return tiktoken.get_encoding("cl100k_base")

    def _count_tokens(self, text: str, model: str) -> int:
        encoding = self._get_encoding(model)
        return len(encoding.encode(text))

    def _truncate_text(self, text: str, max_tokens: int, model: str) -> str:
        encoding = self._get_encoding(model)
        tokens = encoding.encode(text)

        if len(tokens) <= max_tokens:
            return text

        truncated_tokens = tokens[:max_tokens]
        truncated_text = encoding.decode(truncated_tokens)

        if len(tokens) > max_tokens:
            truncated_text += f"\n\n[File truncated - showing first {max_tokens} tokens of {len(tokens)} total tokens]"
        return truncated_text

    def _get_file_info(self, file_obj):
        if isinstance(file_obj, str):
            if not os.path.exists(file_obj):
                raise FileNotFoundError(f"File not found at path: {file_obj}")
            return {
                'name': os.path.basename(file_obj),
                'content_type': mimetypes.guess_type(file_obj)[0],
                'is_path': True,
                'source_obj': file_obj
            }
        elif isinstance(file_obj, FieldFile):
            content_type = getattr(file_obj.file, 'content_type', None) if hasattr(file_obj, 'file') else None
            if not content_type:
                content_type = mimetypes.guess_type(file_obj.name)[0]

            return {
                'name': file_obj.name,
                'content_type': content_type,
                'is_path': False,
                'source_obj': file_obj
            }
        elif isinstance(file_obj, UploadedFile):
            return {
                'name': file_obj.name,
                'content_type': file_obj.content_type,
                'is_path': False,
                'source_obj': file_obj
            }
        else:
            raise ValueError(f"Unsupported file type: {type(file_obj)}. Expected str, FieldFile, or UploadedFile.")

    def _encode_file_for_vision(self, file_obj) -> dict:
        file_info = self._get_file_info(file_obj)

        if file_info['content_type'] and file_info['content_type'].startswith('image/'):
            if file_info['is_path']:
                with open(file_info['source_obj'], "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            else:
                actual_file_to_read = file_info['source_obj']
                actual_file_to_read.seek(0)
                base64_image = base64.b64encode(actual_file_to_read.read()).decode('utf-8')
                actual_file_to_read.seek(0)
            return {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{file_info['content_type']};base64,{base64_image}"
                }
            }
        return None

    def _read_file_content(self, file_obj, model: str, max_file_tokens: int = 50000) -> str:
        file_info = self._get_file_info(file_obj)

        content = ""
        try:
            if file_info['is_path']:
                with open(file_info['source_obj'], 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                actual_file_to_read = file_info['source_obj']
                actual_file_to_read.seek(0)
                raw_content = actual_file_to_read.read()
                actual_file_to_read.seek(0)

                if isinstance(raw_content, bytes):
                    try:
                        content = raw_content.decode('utf-8')
                    except UnicodeDecodeError:
                        content = raw_content.decode('latin-1')
                else:
                    content = raw_content

            return self._truncate_text(content, max_file_tokens, model)

        except UnicodeDecodeError:
            if file_info['is_path']:
                with open(file_info['source_obj'], 'r', encoding='latin-1') as f:
                    content = f.read()
                return self._truncate_text(content, max_file_tokens, model)
            else:
                raise
        except Exception as e:
            raise IOError(f"Failed to read content from file {file_info['name']}: {e}") from e

    def _calculate_message_tokens(self, messages: list, model: str) -> int:
        total_tokens = 0
        for message in messages:
            if isinstance(message['content'], str):
                total_tokens += self._count_tokens(message['content'], model)
            elif isinstance(message['content'], list):
                for content_item in message['content']:
                    if content_item.get('type') == 'text':
                        total_tokens += self._count_tokens(content_item['text'], model)
                    elif content_item.get('type') == 'image_url':
                        total_tokens += 765
        return total_tokens

    def _trim_chat_history(self, messages: list, model: str, max_tokens: int) -> list:
        if self._calculate_message_tokens(messages, model) <= max_tokens:
            return messages

        system_message = None
        if messages and messages[0]['role'] == 'system':
            system_message = messages[0]
            messages_to_trim = messages[1:]
        else:
            messages_to_trim = messages

        user_current_message = None
        if messages_to_trim and messages_to_trim[-1]['role'] == 'user':
            user_current_message = messages_to_trim[-1]
            messages_to_trim = messages_to_trim[:-1]

        current_tokens = 0
        if system_message:
            current_tokens += self._count_tokens(system_message['content'], model)
        if user_current_message:
            current_tokens += self._calculate_message_tokens([user_current_message], model)

        result_messages = []
        if system_message:
            result_messages.append(system_message)

        for message in reversed(messages_to_trim):
            message_tokens = self._calculate_message_tokens([message], model)
            if current_tokens + message_tokens <= max_tokens:
                result_messages.insert(-1 if user_current_message else len(result_messages), message)
                current_tokens += message_tokens
            else:
                break

        if user_current_message:
            result_messages.append(user_current_message)

        return result_messages

    def send_request(self, system_prompt: str, **kwargs):
        try:
            user_data = kwargs.get("data", "")
            chat_history = kwargs.get("chat_history", [])
            model = kwargs.get("model", "gpt-4o-mini-2024-07-18")
            db_file = kwargs.get("file", None)

            messages = [{"role": "system", "content": system_prompt}]

            if chat_history:
                for chat in chat_history:
                    role = "assistant" if chat.sender == enums.ChatSenderType.AI else "user"
                    messages.append({
                        "role": role,
                        "content": chat.text
                    })

            user_message_content = []
            if user_data:
                user_message_content.append({
                    "type": "text",
                    "text": user_data
                })

            if db_file:
                try:
                    file_info = self._get_file_info(db_file)

                    image_content = self._encode_file_for_vision(db_file)

                    if image_content:
                        user_message_content.append(image_content)
                    else:
                        system_tokens = self._count_tokens(system_prompt, model)
                        user_text_tokens = self._count_tokens(user_data, model) if user_data else 0

                        chat_history_tokens = 0
                        for chat in chat_history:
                            chat_history_tokens += self._count_tokens(chat.text, model)

                        used_tokens = system_tokens + user_text_tokens + chat_history_tokens
                        remaining_tokens = self.max_tokens - used_tokens - 1000

                        max_file_tokens = max(10000, min(50000, remaining_tokens))

                        file_content = self._read_file_content(db_file, model, max_file_tokens)
                        file_text = f"\n\nFile content ({file_info['name']}):\n{file_content}"

                        if user_message_content:
                            if user_message_content[0]["type"] == "text":
                                user_message_content[0]["text"] += file_text
                            else:
                                user_message_content.append({"type": "text", "text": file_text})
                        else:
                            user_message_content.append({
                                "type": "text",
                                "text": file_text
                            })
                except (FileNotFoundError, ValueError, IOError) as file_error:
                    error_text = f"\n\nError processing file: {str(file_error)}"
                    if user_message_content:
                        user_message_content[0]["text"] += error_text
                    else:
                        user_message_content.append({
                            "type": "text",
                            "text": error_text
                        })
                except Exception as e:
                    error_text = f"\n\nAn unexpected error occurred while processing the file: {str(e)}"
                    if user_message_content:
                        user_message_content[0]["text"] += error_text
                    else:
                        user_message_content.append({
                            "type": "text",
                            "text": error_text
                        })

            if user_message_content:
                if len(user_message_content) == 1 and user_message_content[0]["type"] == "text":
                    messages.append({
                        "role": "user",
                        "content": user_message_content[0]["text"]
                    })
                else:
                    messages.append({
                        "role": "user",
                        "content": user_message_content
                    })

            total_tokens = self._calculate_message_tokens(messages, model)
            if total_tokens > self.max_tokens:
                messages = self._trim_chat_history(messages, model, self.max_tokens)

            completion_kwargs = {
                "model": model,
                "messages": messages
            }

            response = self.client.chat.completions.create(**completion_kwargs)
            content = response.choices[0].message.content

            return content

        except openai.OpenAIError as e:
            return {"error": f"OpenAI API error: {str(e)}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred in send_request: {str(e)}"}