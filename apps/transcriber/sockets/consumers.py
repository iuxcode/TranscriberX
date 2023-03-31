import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from apps.transcriber.services.ai import OpenAI


class TranscriptConsumer(AsyncJsonWebsocketConsumer):
    ai = OpenAI()

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """

        """ # Are they logged in?
        if self.scope["user"].is_anonymous:
            await self.close()  # Reject the connection
        else:
            await self.accept()  # Accept the connection
            await self.send_json({"type": "websocket.accept"}) """

        await self.accept()
        await self.send_json({"type": "websocket.accept"})

    async def receive_json(self, content, **kwargs):
        audio = content["audio"]

        if audio is None:
            await self.send_json({"type": "websocket.error", "error": "audio chunck is required!!"})

        await self.send_json({"type": "websocket.send", "content": content})
