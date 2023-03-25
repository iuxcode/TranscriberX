from django.urls import path
from .views import UserAPIViewSet, SubscriptionPlanViewSet, ProjectAPIViewSet, APIKeyViewSet

urlpatterns = [
    path("users", UserAPIViewSet.as_view({"get": "list"})),
    path("users/create", UserAPIViewSet.as_view({"post": "create"})),
    path("projects", ProjectAPIViewSet.as_view({"get": "list"})),
    path("projects/create", ProjectAPIViewSet.as_view({"post": "create"})),
    path("keys", APIKeyViewSet.as_view({"get": "list"})),
    path("subscriptions/plans", SubscriptionPlanViewSet.as_view({"get": "list"})),
]
