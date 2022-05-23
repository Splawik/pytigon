from django.core.management.base import BaseCommand
from pytigon_lib.schtools.install import import_from_local_db


class Command(BaseCommand):
    help = "Export default database to local sqlite database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--withoutapp",
            help="do not export applications",
        )

    def handle(self, *args, **options):
        if "withoutapp" in options and options["withoutapp"]:
            withoutapp = options["withoutapp"].split(";")
        else:
            withoutapp = None

        import_from_local_db(withoutapp)
