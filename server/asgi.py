"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import apps.transcriber.sockets.routing
from apps.transcriber.sockets.middleware import ApiKeyAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            ApiKeyAuthMiddleware(
                URLRouter(
                    apps.transcriber.sockets.routing.websocket_urlpatterns,
                )
            )
        ),
    }
)
