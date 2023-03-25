from rest_framework import viewsets
from . import models
from . import serializers


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class ProjectAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = models.APIKey.objects.all()
    serializer_class = serializers.APIKeySerializer

    def get_queryset(self):
        return models.APIKey.objects.all()


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = models.SubscriptionPlan.objects.all()
    serializer_class = serializers.SubscriptionPlanSerializer
