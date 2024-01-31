from django.core.management.commands import makemigrations
from django.conf import settings


class Command(makemigrations.Command):
    help = "Make migrations for all applications"

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            if type(app) == str:
                app_name = app
            else:
                app_name = app.name
            app_name = app_name.split(".")[-1]
            print(app_name)
            super().handle(app_name, **options)
