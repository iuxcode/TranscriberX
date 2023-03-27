from django.shortcuts import get_list_or_404
from rest_framework import viewsets, generics, exceptions
from . import models
from . import serializers


class UserAPIViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserProjectsAPIView(generics.ListAPIView):
    serializer_class = serializers.ProjectSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        queryset = models.Project.objects.all()
        user_id = self.kwargs.get(self.lookup_url_kwarg)

        return get_list_or_404(queryset, user_id=user_id)


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
