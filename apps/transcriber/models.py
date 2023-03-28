import uuid
import os
from django.db import models
from django_extensions.db.models import TimeStampedModel
from server import settings


class Transcription(TimeStampedModel):
    """
    Store information about transcribed audio.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to=os.path.join(settings.AUDIO_UPLOAD_URL, "transcribed"))
    audio_original_name = models.TextField()
    transcription = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    confidence_score = models.FloatField(null=True)

    class Meta:
        verbose_name = "Transcription"
        verbose_name_plural = "Transcriptions"
