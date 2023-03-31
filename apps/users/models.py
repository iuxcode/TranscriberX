import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel, ActivatorModel
from rest_framework_api_key.models import AbstractAPIKey
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, ActivatorModel):
    """
    Store information about registered users.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=False, null=False)
    subscription_plan = models.ForeignKey("SubscriptionPlan", on_delete=models.PROTECT)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_sign_in = models.DateTimeField(_("last sign in"), null=True, blank=False)
    is_staff = models.BooleanField(_("is staff"), default=False)
    created = None

    object = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} [{self.email}]"


class Project(TitleDescriptionModel, TimeStampedModel):
    """
    Store project information's.
    * Each apps calling this API is considered as user project
    * Each app (project) can use his [api_key] to authenticate his requests.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.TextField()

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
