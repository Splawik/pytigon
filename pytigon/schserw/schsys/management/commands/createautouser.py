from django.contrib.auth.management.commands import createsuperuser
from django.db import DEFAULT_DB_ALIAS


class Command(createsuperuser.Command):
    help = "Crate a auto user (superuser)"

    def handle(self, *args, **options):
        d = {self.UserModel.USERNAME_FIELD: "auto"}
        # user = self.UserModel.objects.filter(username="auto")
        user = self.UserModel.objects.filter(**d)
        if not user:
            super(Command, self).handle(
                username="auto",
                database=DEFAULT_DB_ALIAS,
                email="none@none.none",
                interactive=False,
                noinput=True,
                verbosity=False,
            )
        # user = self.UserModel.objects.get(username="auto")
        user = self.UserModel.objects.filter(**d)
        user.set_password("anawa")
        user.save()
