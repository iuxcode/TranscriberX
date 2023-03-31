from django.contrib.auth.hashers import make_password
from rest_framework_json_api import serializers
from rest_framework_api_key.models import APIKey
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
    subscription_plan = SubscriptionPlanSerializer(many=False, read_only=True)
    subscription_plan_id = serializers.IntegerField(
        write_only=True, default=settings.DEFAULT_SUBSCRIPTION_PLAN_ID
    )
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = [
            "username",
            "email",
            "password",
            "subscription_plan",
            "subscription_plan_id",
            "created",
            "modified",
            "status",
            "activate_date",
            "deactivate_date",
        ]

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="title")
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.UUIDField(write_only=True)
    api_key = serializers.CharField(read_only=True)

    class Meta:
        model = models.Project
        fields = ["name", "description", "api_key", "user", "user_id", "created", "modified"]

    def create(self, validated_data):
        try:
            _, key = APIKey.objects.create_key(name=validated_data.get("title"))
            project = models.Project(**validated_data, api_key=key)
            project.save()
            return project
        except Exception as e:
            raise e


class UsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Usage
        fields = ["user", "endpoint", "request_data", "response_data", "response_time"]
