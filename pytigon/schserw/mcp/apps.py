from django.apps import AppConfig


class MCPConfig(AppConfig):
    name = "pytigon.schserw.mcp"
    label = "mcp"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        from .registry import init

        init()
