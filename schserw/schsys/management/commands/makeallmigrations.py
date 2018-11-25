from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands import makemigrations
from django.conf import settings

class Command(makemigrations.Command):
    help = 'Make migrations for all applications'

    def handle(self, *args, **options):
        for app in settings.INSTALLED_APPS:
            if type(app) == str:
                app_name = app
            else:
                app_name = app.name

            print(app_name)

            options2 = options.copy()
            options2['name'] =  app_name
            super().handle(*args, **options2)
