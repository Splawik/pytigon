from django.core.management.base import BaseCommand, CommandError
from schlib.schtools.install import export_to_local_db


class Command(BaseCommand):
    help = 'Export default database to local sqlite database'

    def handle(self, *args, **options):
        export_to_local_db()
            
