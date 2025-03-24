import elevenlabs
from django.conf import settings


class ElevenLabCli:
    def __init__(self):
        self.elevenlab = elevenlabs.ElevenLabs(
            api_key=settings.ELEVENLAB_API_KEY
        )
        self.voice = "George"
        self.model = "eleven_multilingual_v2"

    def send_request(self, text):
        voice = self.elevenlab.generate(
            text=text,
            voice=self.voice,
            stream=False,
            model=self.model,
        )
        chunks = b""
        for chunk in voice:
            chunks += chunk
        return chunks
