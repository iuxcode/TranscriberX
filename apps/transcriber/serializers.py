from rest_framework_json_api import serializers
from . import models


class TranscriptionSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(write_only=True, required=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Transcription
        fields = [
            "id",
            "user",
            "user_id",
            "audio_file",
            "audio_original_name",
            "transcription",
            "start_time",
            "end_time",
            "confidence_score",
        ]
