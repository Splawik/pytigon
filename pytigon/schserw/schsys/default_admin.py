"""Production guard for the default administrator account.

Pytigon deliberately ships a well-known bootstrap administrator
(``auto`` / ``anawa``). A local desktop installation must be usable without a
login, and an application package carries data owned by a known account, so the
bootstrap credential is a **documented default, not a secret**.

The security control therefore does not live in the credential but at the
network boundary: an internet-facing production deployment must not keep
serving with the bootstrap password. This module provides:

* :func:`is_production_webserver` — whether the current process is a production
  web server (as opposed to the embedded desktop client or a shell command);
* :func:`default_admin_is_active` — whether the bootstrap account still has the
  bootstrap password;
* :func:`startup_check` — one loud warning per process at startup, or a hard
  stop when ``PYTIGON_STRICT_DEFAULT_ADMIN`` is enabled;
* :func:`user_has_default_password` — a cheap, cached check used by the
  middleware to force a password change in production.

Nothing here runs in the local/embedded mode: it must not add any friction to a
single-user desktop application.
"""

import logging
import threading

from django.conf import settings

logger = logging.getLogger(__name__)

# One startup decision per process. The lock also keeps two concurrent first
# requests from both emitting the banner.
_startup_lock = threading.Lock()
_startup_done = False
_startup_blocked = False

# Per-process cache for user_has_default_password(), keyed by primary key. The
# stored password hash is part of the value, so a password change invalidates
# the entry automatically on the next request.
_password_cache: dict = {}
_password_lock = threading.Lock()

_HINT = (
    "Change the password before exposing this server: "
    "ptig manage_<project> changepassword <user>, "
    "or set PYTIGON_STRICT_DEFAULT_ADMIN=1 to refuse to start instead."
)


def default_admin_username() -> str:
    """Return the configured bootstrap administrator username."""
    return getattr(settings, "DEFAULT_ADMIN_USERNAME", "auto")


def default_admin_password() -> str:
    """Return the configured bootstrap administrator password."""
    return getattr(settings, "DEFAULT_ADMIN_PASSWORD", "anawa")


def is_production_webserver() -> bool:
    """Return True only for a production web-server deployment.

    The embedded desktop client and development servers must never trigger the
    default-administrator guard. ``PLATFORM_TYPE`` is ``"webserver"`` only when
    the application runs from the production web location; ``PRODUCTION_VERSION``
    and ``DEBUG`` filter out management commands and development runs.
    """
    return bool(
        getattr(settings, "PRODUCTION_VERSION", False)
        and not getattr(settings, "DEBUG", False)
        and getattr(settings, "PLATFORM_TYPE", "") == "webserver"
    )


def default_admin_is_active(database: str = "default"):
    """Return whether the bootstrap account still uses the bootstrap password.

    Returns:
        ``True`` when the account exists and its password is the configured
        bootstrap password, ``False`` when it is absent or already changed, and
        ``None`` when the answer cannot be determined (for example before the
        auth tables exist).
    """
    from django.contrib.auth import get_user_model
    from django.db import DatabaseError

    user_model = get_user_model()
    try:
        user = (
            user_model.objects.using(database)
            .filter(**{user_model.USERNAME_FIELD: default_admin_username()})
            .first()
        )
    except DatabaseError:
        return None

    if user is None:
        return False
    try:
        return bool(user.check_password(default_admin_password()))
    except Exception:  # noqa: BLE001 - a broken hash must not crash startup
        return None


def user_has_default_password(user) -> bool:
    """Return whether *user* is the bootstrap administrator on its default password.

    Hashing a password with PBKDF2 is intentionally slow, so the result is
    cached per process and invalidated when the stored password hash changes
    (i.e. after the password is changed).
    """
    if not getattr(user, "is_authenticated", False):
        return False

    field = getattr(user, "USERNAME_FIELD", "username")
    if getattr(user, field, None) != default_admin_username():
        return False

    key = user.pk
    digest = user.password
    with _password_lock:
        cached = _password_cache.get(key)
        if cached is not None and cached[0] == digest:
            return cached[1]

    result = bool(user.check_password(default_admin_password()))
    with _password_lock:
        _password_cache[key] = (digest, result)
    return result


def startup_check(raise_if_blocked: bool = False) -> str:
    """Run the default-administrator guard once per process.

    Args:
        raise_if_blocked: When True (the ASGI entry point), a strict-mode block
            raises :class:`~django.core.exceptions.ImproperlyConfigured` so the
            server refuses to boot. When False (middleware), the caller turns
            the ``"blocked"`` result into a 503 response.

    Returns:
        ``"ok"``, ``"warned"`` or ``"blocked"``.
    """
    global _startup_done, _startup_blocked

    with _startup_lock:
        if _startup_done:
            return "blocked" if _startup_blocked else "ok"
        _startup_done = True

        if not is_production_webserver():
            return "ok"

        if not default_admin_is_active():
            return "ok"

        message = (
            f"SECURITY: the default administrator account "
            f"{default_admin_username()!r} still uses its well-known bootstrap "
            f"password. This installation is running as a production web "
            f"server. {_HINT}"
        )

        if getattr(settings, "PYTIGON_STRICT_DEFAULT_ADMIN", False):
            _startup_blocked = True
            logger.critical(message)
            if raise_if_blocked:
                from django.core.exceptions import ImproperlyConfigured

                raise ImproperlyConfigured(message)
            return "blocked"

        logger.critical(message)
        return "warned"


def reset_startup_check() -> None:
    """Reset the one-shot startup guard (used by tests)."""
    global _startup_done, _startup_blocked

    with _startup_lock:
        _startup_done = False
        _startup_blocked = False
    with _password_lock:
        _password_cache.clear()
