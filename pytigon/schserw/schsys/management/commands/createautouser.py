from django.contrib.auth.management.commands import createsuperuser
from django.db import DEFAULT_DB_ALIAS
from pytigon_lib.schtools.env import get_environ


class Command(createsuperuser.Command):
    help = "Crate a auto user (superuser)"

    def handle(self, *args, **options):
        env = get_environ()
        username = env("USERNAME")
        password = env("PASSWORD")
        d = {self.UserModel.USERNAME_FIELD: username}
        user = self.UserModel.objects.filter(**d).first()
        if not user:
            dd = {
                self.UserModel.USERNAME_FIELD: username,
                "database": DEFAULT_DB_ALIAS,
                "interactive": False,
                "noinput": True,
                "verbosity": False,
            }
            if self.UserModel.USERNAME_FIELD != "email":
                dd["email"] = "none@none.none"

            super().handle(**dd)
        user = self.UserModel.objects.filter(**d).first()
        user.set_password(password)
        user.save()
