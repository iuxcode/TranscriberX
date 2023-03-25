import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Transcription(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to="audio_files/")
    transcription = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speaker_id = models.CharField(max_length=50, blank=True)
    confidence_score = models.FloatField(null=True)

    class Meta:
        verbose_name = "Transcription"
        verbose_name_plural = "Transcriptions"
