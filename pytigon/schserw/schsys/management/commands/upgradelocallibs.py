from django.core.management.base import BaseCommand
from pytigon_lib.schtools.install_init import upgrade_local_libs


class Command(BaseCommand):
    help = "Upgrade local libs"

    def handle(self, *args, **options):
        upgrade_local_libs()
