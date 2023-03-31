from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("transcribe", consumers.TranscriptConsumer.as_asgi()),
]
