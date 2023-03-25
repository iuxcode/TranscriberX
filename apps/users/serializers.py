from rest_framework_json_api import serializers
from server import settings
from . import models


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="title")

    class Meta:
        model = models.SubscriptionPlan
        fields = [
            "name",
            "description",
            "price",
            "max_requests",
            "max_audio_duration",
            "features",
            "created",
            "modified",
        ]


class SubscriptionPlanFeatureSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="title")

    class Meta:
        model = models.SubscriptionPlanFeature
        fields = ["name", "description", "created", "modified"]


class UserSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(read_only=True)
    subscription_plan = SubscriptionPlanSerializer(many=False, read_only=True)
    subscription_plan_id = serializers.IntegerField(
        write_only=True, default=settings.DEFAULT_SUBSCRIPTION_PLAN_ID
    )

    class Meta:
        model = models.User
        fields = [
            "username",
            "email",
            "api_key",
            "subscription_plan",
            "subscription_plan_id",
            "created",
            "modified",
            "status",
            "activate_date",
            "deactivate_date",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="title")

    class Meta:
        model = models.Project
        fields = ["name", "description", "api_key", "user", "created", "modified"]


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.APIKey
        fields = [
            "key",
            "app_name",
            "user",
            "created",
            "modified",
            "status",
            "activate_date",
            "deactivate_date",
        ]


class UsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usage
        fields = ["user", "endpoint", "request_data", "response_data", "response_time"]
