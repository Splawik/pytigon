"""Database-backed tests for the bootstrap administrator provisioning.

Kept in a separate module because they need pytest-django's ``django_db``
fixture (a test database). The surrounding test suite runs with a custom
plugin, so the mark is unavailable there and this module is skipped.
"""

import pytest

pytest.importorskip("pytest_django", reason="pytest-django is required for DB tests")


@pytest.mark.django_db
def test_create_only_never_overwrites_password():
    from django.contrib.auth import get_user_model

    from pytigon_lib.schtools.install import ensure_default_admin

    user_model = get_user_model()
    user_model.objects.filter(username="auto").delete()

    created = ensure_default_admin()
    assert created is not None
    assert created.username == "auto"
    assert created.is_superuser is True

    created.set_password("a-changed-strong-password")
    created.save()

    # Second run must not touch the existing account.
    assert ensure_default_admin() is None

    created.refresh_from_db()
    assert created.check_password("a-changed-strong-password")


@pytest.mark.django_db
def test_existing_account_is_not_duplicated():
    from django.contrib.auth import get_user_model

    from pytigon_lib.schtools.install import ensure_default_admin

    user_model = get_user_model()
    user_model.objects.filter(username="auto").delete()
    User = user_model.objects.create_user("auto", password="custom-pass")

    assert ensure_default_admin() is None
    assert user_model.objects.filter(username="auto").count() == 1
    User.refresh_from_db()
    assert User.check_password("custom-pass")
