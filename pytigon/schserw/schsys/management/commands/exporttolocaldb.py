from django.core.management.base import BaseCommand, CommandError
from pytigon_lib.schtools.install import export_to_local_db


class Command(BaseCommand):
    help = "Export default database to local sqlite database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--withoutapp",
            help="do not export applications",
        )

    def handle(self, *args, **options):
        if "withoutapp" in options:
            withoutapp = options["withoutapp"].split(";")
        else:
            withoutapp = None

        export_to_local_db(withoutapp)
