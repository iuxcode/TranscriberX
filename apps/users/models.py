import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel, ActivatorModel
from rest_framework_api_key.models import AbstractAPIKey
from .managers import UserManager


class User(AbstractUser, PermissionsMixin, TimeStampedModel, ActivatorModel):
    """
    Store information about registered users.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=False, null=False)
    subscription_plan = models.ForeignKey("SubscriptionPlan", on_delete=models.PROTECT)
    created = None

    object = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username} [{self.email}]"


class APIKey(AbstractAPIKey):
    """
    Store [project] API keys.
    """

    name = models.CharField(
        max_length=50,
        blank=False,
        default=None,
        unique=True,
        help_text=(
            "A free-form name for the API key. " "Need not be unique. " "50 characters max."
        ),
    )

    class Meta:
        verbose_name = "APIKey"
        verbose_name_plural = "APIKeys"


class Project(TitleDescriptionModel, TimeStampedModel):
    """
    Store project information's.
    * Each apps calling this API is considered as user project
    * Each app (project) can use his [api_key] to authenticate his requests.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class SubscriptionPlan(TitleDescriptionModel, TimeStampedModel):
    """
    Store information about the subscription plans offered.
    """

    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_requests = models.PositiveIntegerField()
    max_audio_duration = models.PositiveIntegerField()
    features = models.ManyToManyField("SubscriptionPlanFeature")

    class Meta:
        verbose_name = "SubscriptionPlan"
        verbose_name_plural = "SubscriptionPlans"


class SubscriptionPlanFeature(TitleDescriptionModel, TimeStampedModel):
    """
    Store information about the features included in each subscription plan.
    """

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"


class Usage(TimeStampedModel):
    """Store usage data for each user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    request_data = models.JSONField()
    response_data = models.JSONField()
    response_time = models.FloatField()

    class Meta:
        verbose_name = "Usage"
        verbose_name_plural = "Usage"
