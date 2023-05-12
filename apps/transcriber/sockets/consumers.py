import base64
import wave
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from server import settings
from apps.transcriber.services.ai import OpenAI


class ResponseCode:
    def __init__(self, code, pointer=None, detail=None):
        self.code = code
        self.pointer = pointer
        self.detail = detail

    def to_json(self):
        json = {"type": f"websocket.{self.code}"}

        if self.pointer is not None:
            json["pointer"] = self.pointer
        if self.detail is not None:
            json["detail"] = self.detail

        return json


class ResponseOk(ResponseCode):
    def __init__(self):
        super().__init__("ok")


class ResponseError(ResponseCode):
    def __init__(self, detail, pointer=None):
        super().__init__("error", detail=detail, pointer=pointer)


class TranscriptConsumer(AsyncJsonWebsocketConsumer):
    ai = OpenAI()

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """

        # Are they logged in?
        if self.scope["user"].is_anonymous:
            await self.close()  # Reject the connection
        else:
            await self.accept()  # Accept the connection
            await self.send_json(ResponseOk().to_json())

    async def disconnect(self, code):
        pass

    async def receive_json(self, content, **kwargs):
        action = content.get("action")

        if action == "transcribe":
            await self.transcribe(content.get("data"))
        else:
            await self.send_json(ResponseError("You must provide an valid action").to_json())

    async def decode_b64_audio(self, b64_str):
        file_path = f"{settings.AUDIO_UPLOAD_URL}/temp/current_live.wav"
        decoded_data = base64.b64decode(b64_str)
        with open(file_path, "wb") as file:
            file.write(decoded_data)

    async def transcribe(self, content):
        if content is None:
            await self.send_json(
                ResponseError(
                    "Invalid request! you must provide data", pointer="body/data"
                ).to_json()
            )
            return

        chunk = content.get("chunk")
        if chunk is not None and len(chunk) > 0:
            audio = await self.decode_b64_audio(chunk)
            await self.send_json(ResponseOk().to_json())
        else:
            await self.send_json(
                ResponseError("audio chunk is required", pointer="body/data/chunk").to_json()
            )
            return
