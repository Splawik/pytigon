from django.contrib.auth.management.commands import createsuperuser
from django.db import DEFAULT_DB_ALIAS


class Command(createsuperuser.Command):
    help = "Crate a auto user (superuser)"

    def handle(self, *args, **options):
        d = {self.UserModel.USERNAME_FIELD: "auto"}
        user = self.UserModel.objects.filter(**d).first()
        if not user:
            dd = {
                self.UserModel.USERNAME_FIELD: "auto",
                "database": DEFAULT_DB_ALIAS,
                "interactive": False,
                "noinput": True,
                "verbosity": False,
            }
            if self.UserModel.USERNAME_FIELD != "email":
                dd["email"] = "none@none.none"

            super(Command, self).handle(**dd)
        user = self.UserModel.objects.filter(**d).first()
        user.set_password("anawa")
        user.save()
