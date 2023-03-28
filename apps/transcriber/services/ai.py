import openai
from server import settings


class OpenAI:
    def __init__(self, *args, **kwargs):
        openai.api_key = settings.OPENAI_API_KEY

    def transcribe(self, file_path):
        audio_file = open(file_path, "rb")
        return openai.Audio.transcribe("whisper-1", audio_file)
