from django.conf import settings
from django.core.management.commands import makemigrations


class Command(makemigrations.Command):
    help = "Make migrations for all applications"

    def handle(self, *args, **options):
        seen_labels = set()
        labels = []
        for app in settings.INSTALLED_APPS:
            app_name = app if isinstance(app, str) else app.name
            label = app_name.split(".")[-1]
            if label in seen_labels:
                continue
            seen_labels.add(label)
            labels.append(label)
        # One pass: calling super().handle() per app re-scans the whole
        # migration state N times. options may still carry its own app_label,
        # which would restrict the run to a single app, so drop it.
        options.pop("app_label", None)
        for label in labels:
            self.stdout.write(label)
        super().handle(*labels, **options)
