from django.urls import path
from . import views

urlpatterns = [
    path(
        "transcribe",
        views.TranscriptionAPIViewSet.as_view({"post": "transcribe"}),
        name="transcribe",
    ),
    path(
        "transcriptions",
        views.TranscriptionAPIViewSet.as_view({"get": "list"}),
        name="transcriptions_list",
    ),
    path(
        "transcriptions/<uuid:pk>",
        views.TranscriptionAPIViewSet.as_view({"get": "retrieve"}),
        name="transcriptions_retrieve",
    ),
    path(
        "transcriptions/delete/<uuid:pk>",
        views.TranscriptionAPIViewSet.as_view({"delete": "destroy"}),
        name="transcriptions_delete",
    ),
]
