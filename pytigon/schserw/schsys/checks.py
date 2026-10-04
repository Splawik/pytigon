"""System checks for the default administrator account.

Registered on import; :mod:`pytigon.schserw.schsys` imports this module so the
check is available to ``manage.py check`` / ``check --deploy`` without an
``AppConfig`` (Pytigon builds its app configs dynamically).
"""

from django.core.checks import Tags, Warning, register

from . import default_admin


@register(Tags.security, deploy=True)
def default_admin_credentials(app_configs, **kwargs):
    """Warn when a production server still uses the bootstrap admin password."""
    if not default_admin.is_production_webserver():
        return []

    if default_admin.default_admin_is_active():
        return [
            Warning(
                f"The default administrator account "
                f"{default_admin.default_admin_username()!r} still uses the "
                f"well-known bootstrap password.",
                hint=(
                    "Change it before exposing this server to the network: "
                    "ptig manage_<project> changepassword <user>. "
                    "Set PYTIGON_STRICT_DEFAULT_ADMIN=1 to refuse to start instead."
                ),
                id="pytigon.W001",
            )
        ]
    return []
