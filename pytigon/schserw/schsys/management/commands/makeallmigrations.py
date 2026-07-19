from django.conf import settings
from django.core.management.commands import makemigrations


class Command(makemigrations.Command):
    help = "Make migrations for all applications"

    def handle(self, *args, **options):
        seen_labels = set()
        for app in settings.INSTALLED_APPS:
            app_name = app if isinstance(app, str) else app.name
            label = app_name.split(".")[-1]
            if label in seen_labels:
                continue
            seen_labels.add(label)
            print(label)
            super().handle(label, **options)
