from django.contrib.auth.base_user import BaseUserManager
from server import settings
from . import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email!")
        if not password:
            raise ValueError("User must have a password!")

        subscription_plan = models.SubscriptionPlan.objects.get(
            pk=settings.DEFAULT_SUBSCRIPTION_PLAN_ID
        )
        if not subscription_plan:
            raise ValueError(
                "Subscription plan with {settings.DEFAULT_SUBSCRIPTION_PLAN_ID} ID not found! Make sure there are existing plans!!!"
            )

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            subscription_plan=subscription_plan,
            **extra_fields,
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)
