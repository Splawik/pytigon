from django.core.management.base import BaseCommand, CommandError
from pytigon_lib.schtools.install import install


class Command(BaseCommand):
    help = "Post installation steps"

    def handle(self, *args, **options):
        install()
