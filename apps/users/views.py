from django.shortcuts import get_list_or_404
from rest_framework import viewsets, generics, exceptions, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from . import models, serializers


class AuthenticationAPIViewSet(viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_user(self, data, lookup_field="username"):
        try:
            return (
                self.get_queryset().get(username=data)
                if (lookup_field == "username")
                else self.get_queryset().get(email=data)
            )
        except models.User.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed(
                "No active user has been found with the provided credentials"
            ) from exc

    def generate_token_for(self, serialized_user):
        user = self.get_user(serialized_user.data["username"])
        refresh = RefreshToken.for_user(user)

        return {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "user": serialized_user.data,
        }

    def authenticate(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        user = None

        # Validate auth provider
        # Can be username | email
        if username is not None and len(username) > 0:
            user = self.get_user(username)
        elif email is not None and len(email) > 0:
            user = self.get_user(email, lookup_field="email")
        else:
            raise exceptions.ValidationError("Login must be Username based or Email based")

        # return Unauthorized 401 if there no user registered with provided username or email
        if user is None:
            raise exceptions.AuthenticationFailed(
                "No active user has been found with the provided credentials"
            )

        # Validate password
        if password is not None and user.check_password(password):
            return Response(self.generate_token_for(self.get_serializer(user)))
        else:
            raise exceptions.AuthenticationFailed("Invalid password")

    def register(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(self.generate_token_for(serializer))


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


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = models.SubscriptionPlan.objects.all()
    serializer_class = serializers.SubscriptionPlanSerializer
