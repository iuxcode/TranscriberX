import os
from django.utils import timezone
from rest_framework import viewsets, parsers, permissions, exceptions
from rest_framework.response import Response
from server import settings
from .services.ai import OpenAI
from . import models, serializers

class TranscriptionAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Transcription.objects.all()
    serializer_class = serializers.TranscriptionSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    ai = OpenAI()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [permissions.AllowAny] if self.action == "transcribe" else []
        return [permission() for permission in permission_classes]

    def handle_uploaded_file(self, file):
        upload_path = os.path.join(settings.AUDIO_UPLOAD_URL, "temp")
        upload_path_exist = os.path.exists(upload_path)

        if not upload_path_exist:
            os.makedirs(upload_path)  # Create a new directory because it does not exist
            self.handle_uploaded_file(file)
        else:
            destination = open(f"{upload_path}/{file.name}", "wb+")
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

        return f"{upload_path}/{file.name}"

    def transcribe(self, request):
        audio_file = request.FILES.get("audio")
        user_id = request.data.get("user_id")

        if audio_file is None:
            raise exceptions.ValidationError("audio field is required")
        if user_id is None:
            raise exceptions.ValidationError("user_id field is required")
        if (
            "".join(os.path.splitext(audio_file.name)[1].lower().split("."))
            not in settings.TRANSCRIPTION_SUPPORTED_AUDIO
        ):
            raise exceptions.ValidationError(
                f"invalid audio file! supported format are {settings.TRANSCRIPTION_SUPPORTED_AUDIO}"
            )

        audio_original_name = audio_file.name
        audio_path = self.handle_uploaded_file(audio_file)
        start_time = timezone.now()
        transcription = self.ai.transcribe(audio_path).text

        serializer = self.get_serializer(
            data={
                "user_id": user_id,
                "audio_original_name": audio_original_name,
                "audio_file": audio_file,
                "transcription": transcription,
                "start_time": start_time,
                "end_time": timezone.now(),
                "confidence_score": 1,
            }
        )

        os.remove(audio_path)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
