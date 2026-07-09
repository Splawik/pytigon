"""Tests for pytigon.schserw.settings.__init__ module."""

from unittest.mock import MagicMock, patch

import pytest


class TestSettingsInit:
    def test_finish_sets_login_redirect_url(self):
        """finish() sets LOGIN_REDIRECT_URL to /{URL_ROOT_FOLDER}/ (overwrites old value - see source bug)."""
        from pytigon.schserw.settings import finish

        settings = MagicMock()
        settings.__getitem__ = lambda self, k: getattr(self, k, "")
        settings.__setitem__ = lambda self, k, v: setattr(self, k, v)
        settings.URL_ROOT_FOLDER = "app"
        settings.LOGIN_REDIRECT_URL = "/default/"

        finish(settings)
        assert settings.LOGIN_REDIRECT_URL is not None
        assert "app" in settings.LOGIN_REDIRECT_URL

    def test_finish_without_url_root_folder(self):
        from pytigon.schserw.settings import finish

        settings = MagicMock()
        settings.__getitem__ = lambda self, k: getattr(self, k, "")
        settings.__setitem__ = lambda self, k, v: setattr(self, k, v)
        settings.URL_ROOT_FOLDER = ""
        settings.LOGIN_REDIRECT_URL = "/default/"

        finish(settings)
        assert settings.LOGIN_REDIRECT_URL == "/default/"
