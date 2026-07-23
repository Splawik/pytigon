# myapp/management/commands/create_access_token.py
import datetime
import secrets
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from oauth2_provider.models import get_access_token_model, get_application_model

AccessToken = get_access_token_model()
Application = get_application_model()
User = get_user_model()


class Command(BaseCommand):
    """
    Management command to create an OAuth2 access token for a given application.
    """

    help = "Creates an access token for an existing OAuth2 application."

    def add_arguments(self, parser):
        parser.add_argument(
            "application",
            type=str,
            help="Name of the existing OAuth2 application.",
        )
        parser.add_argument(
            "--user",
            type=str,
            default=None,
            help="Username to assign the token to (optional).",
        )
        parser.add_argument(
            "--scope",
            type=str,
            default="read write",
            help="Token scope (default: 'read write').",
        )
        parser.add_argument(
            "--expires-days",
            type=int,
            default=None,
            help="Token validity period in days (optional, defaults to DOT settings).",
        )

    def handle(self, *args, **options):
        app_name = options["application"]
        username = options["user"]
        scope = options["scope"]
        expires_days = options["expires_days"]

        # Retrieve the application
        try:
            application = Application.objects.get(name=app_name)
        except Application.DoesNotExist:
            available = Application.objects.values_list("name", flat=True)
            raise CommandError(
                f"Application '{app_name}' does not exist. "
                f"Available applications: {', '.join(available) or 'none'}"
            )

        # Retrieve the user (optional)
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f"User '{username}' does not exist.")

        # Calculate expiration date
        expires = None
        if expires_days is not None:
            expires = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
                days=expires_days
            )

        print("A1")
        # Create the token
        token_string = secrets.token_hex(16)
        token = AccessToken.objects.create(
            user=user, application=application, scope=scope, expires=expires, token=token_string
        )
        print("A2")

        self.stdout.write(self.style.SUCCESS("Token created successfully!"))
        self.stdout.write(f"  Token:    {token.token}")
        self.stdout.write(f"  App:      {application.name}")
        self.stdout.write(f"  User:     {user.username if user else '(none)'}")
        self.stdout.write(f"  Scope:    {token.scope}")
        self.stdout.write(f"  Expires:  {token.expires or '(per DOT settings)'}")
