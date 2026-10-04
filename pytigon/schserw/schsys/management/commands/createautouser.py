from django.contrib.auth.management.commands import createsuperuser

from pytigon_lib.schtools.install import ensure_default_admin


class Command(createsuperuser.Command):
    help = "Create the default (auto) superuser if it does not exist"

    def handle(self, *args, **options):
        # Create-only. The bootstrap administrator is a documented default, so
        # re-running this command must never reset a password the operator has
        # already changed.
        ensure_default_admin()
