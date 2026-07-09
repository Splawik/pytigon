"""Tests for pytigon.schserw.settings.features module - extended."""

import pytest


class TestSettingsFeaturesExtended:
    def test_installed_apps_structure(self):
        from pytigon.schserw.settings.features import INSTALLED_APPS

        assert isinstance(INSTALLED_APPS, (list, tuple))
        assert len(INSTALLED_APPS) > 5
        assert "django.contrib.auth" in INSTALLED_APPS
        assert "pytigon.schserw.schsys" in INSTALLED_APPS

    def test_middleware_contains_key_entries(self):
        from pytigon.schserw.settings.features import MIDDLEWARE

        assert len(MIDDLEWARE) >= 5
        found_session = any("SessionMiddleware" in m for m in MIDDLEWARE)
        found_auth = any("AuthenticationMiddleware" in m for m in MIDDLEWARE)
        found_common = any("CommonMiddleware" in m for m in MIDDLEWARE)
        assert found_session
        assert found_auth
        assert found_common

    def test_template_loaders(self):
        from pytigon.schserw.settings.features import TEMPLATES

        loaders = TEMPLATES[0]["OPTIONS"]["loaders"]
        assert len(loaders) >= 2

    def test_context_processors_list(self):
        from pytigon.schserw.settings.features import TEMPLATES

        cps = TEMPLATES[0]["OPTIONS"]["context_processors"]
        assert "pytigon.schserw.schsys.context_processors.sch_standard" in cps

    def test_channels_url_tab(self):
        from pytigon.schserw.settings.features import CHANNELS_URL_TAB

        assert isinstance(CHANNELS_URL_TAB, list)
