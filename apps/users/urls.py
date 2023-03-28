from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

urlpatterns = [
    path(
        "login",
        views.AuthenticationAPIViewSet.as_view({"post": "authenticate"}),
        name="authenticate",
    ),
    path(
        "register",
        views.AuthenticationAPIViewSet.as_view({"post": "register"}),
        name="register",
    ),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("users", views.UserAPIViewSet.as_view({"get": "list"})),
    path("users/create", views.UserAPIViewSet.as_view({"post": "create"})),
    path("users/<uuid:pk>/projects", views.UserProjectsAPIView.as_view()),
    path("projects", views.ProjectAPIViewSet.as_view({"get": "list"})),
    path("projects/<uuid:pk>", views.ProjectAPIViewSet.as_view({"get": "retrieve"})),
    path("projects/create", views.ProjectAPIViewSet.as_view({"post": "create"})),
    path("keys", views.APIKeyViewSet.as_view({"get": "list"})),
    path("subscriptions/plans", views.SubscriptionPlanViewSet.as_view({"get": "list"})),
]
