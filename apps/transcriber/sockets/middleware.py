from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from apps.users.models import Project, User


@database_sync_to_async
def return_user(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        return AnonymousUser


@database_sync_to_async
def return_project(api_key):
    try:
        return Project.objects.get(api_key=api_key)
    except Project.DoesNotExist:
        return None


class ApiKeyAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_dict = parse_qs(scope["query_string"].decode())
        key = query_dict.get("key")[0] if "key" in query_dict else None

        project = await return_project(key)

        if project is None:
            scope["user"] = AnonymousUser
            return await super().__call__(scope, receive, send)

        user = await return_user(project.user_id)
        scope["user"] = user
        return await super().__call__(scope, receive, send)
