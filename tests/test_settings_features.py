"""Tests for pytigon.schserw.settings.features module."""

import os
from unittest.mock import patch

import pytest


class TestSettingsFeatures:
    def test_root_urlconf(self):
        from pytigon.schserw.settings.features import ROOT_URLCONF

        assert ROOT_URLCONF == "pytigon.schserw.urls"

    def test_templates_configured(self):
        from pytigon.schserw.settings.features import TEMPLATES

        assert len(TEMPLATES) > 0
        assert "DIRS" in TEMPLATES[0]
        assert "OPTIONS" in TEMPLATES[0]
        assert "context_processors" in TEMPLATES[0]["OPTIONS"]
        assert "loaders" in TEMPLATES[0]["OPTIONS"]

    def test_staticfiles_finders(self):
        from pytigon.schserw.settings.features import STATICFILES_FINDERS

        assert len(STATICFILES_FINDERS) >= 2

    def test_staticfiles_app_installed(self):
        from pytigon.schserw.settings.features import INSTALLED_APPS

        assert "django.contrib.staticfiles" in INSTALLED_APPS

    def test_auth_backends_default(self):
        from pytigon.schserw.settings.features import AUTHENTICATION_BACKENDS

        assert "django.contrib.auth.backends.ModelBackend" in AUTHENTICATION_BACKENDS

    def test_default_auto_field(self):
        from pytigon.schserw.settings.features import DEFAULT_AUTO_FIELD

        assert DEFAULT_AUTO_FIELD == "django.db.models.AutoField"

    def test_prjs_is_list(self):
        from pytigon.schserw.settings.features import PRJS

        assert isinstance(PRJS, list)

    def test_hide_apps_is_list(self):
        from pytigon.schserw.settings.features import HIDE_APPS

        assert isinstance(HIDE_APPS, list)

    def test_channels_url_tab_is_list(self):
        from pytigon.schserw.settings.features import CHANNELS_URL_TAB

        assert isinstance(CHANNELS_URL_TAB, list)

    def test_middleware_configured(self):
        from pytigon.schserw.settings.features import MIDDLEWARE

        assert len(MIDDLEWARE) > 0
        assert "django.contrib.sessions.middleware.SessionMiddleware" in MIDDLEWARE

    def test_locale_paths(self):
        from pytigon.schserw.settings.features import LOCALE_PATHS

        assert len(LOCALE_PATHS) > 0
        for p in LOCALE_PATHS:
            assert isinstance(p, str)

    def test_form_renderer(self):
        from pytigon.schserw.settings.features import FORM_RENDERER

        assert FORM_RENDERER == "django.forms.renderers.TemplatesSetting"
