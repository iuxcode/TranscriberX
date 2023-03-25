from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin
from .models import APIKey


@admin.register(APIKey)
class ProjectAPIKeyModelAdmin(APIKeyModelAdmin):
    pass
