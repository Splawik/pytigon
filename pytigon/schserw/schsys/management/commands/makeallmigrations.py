from django.conf import settings
from django.core.management.commands import makemigrations


class Command(makemigrations.Command):
    help = "Make migrations for all applications"

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            app_name = app if type(app) == str else app.name
            app_name = app_name.split(".")[-1]
            print(app_name)
            super().handle(app_name, **options)
