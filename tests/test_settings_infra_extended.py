"""Extended tests for pytigon.schserw.settings.infra module."""

import os
from unittest.mock import patch

import pytest


class TestSettingsInfraExtended:
    def test_logging_configured(self):
        from pytigon.schserw.settings.infra import LOGGING

        assert isinstance(LOGGING, dict)
        assert "version" in LOGGING

    def test_channel_layers(self):
        from pytigon.schserw.settings.infra import CHANNEL_LAYERS

        assert "default" in CHANNEL_LAYERS
        assert "BACKEND" in CHANNEL_LAYERS["default"]

    def test_cors_origin_whitelist(self):
        from pytigon.schserw.settings.infra import CORS_ORIGIN_WHITELIST

        assert isinstance(CORS_ORIGIN_WHITELIST, (list, tuple))

    def test_allowed_hosts(self):
        from pytigon.schserw.settings.infra import ALLOWED_HOSTS

        assert isinstance(ALLOWED_HOSTS, (list, tuple))

    def test_secure_settings(self):
        from pytigon.schserw.settings.infra import (
            SECURE_PROXY_SSL_HEADER,
            SECURE_REFERRER_POLICY,
            SECURE_SSL_REDIRECT,
            X_FRAME_OPTIONS,
        )

        assert isinstance(X_FRAME_OPTIONS, str)
        assert isinstance(SECURE_REFERRER_POLICY, str)
        # Env-driven in both branches so a TLS-terminating proxy is detected.
        assert isinstance(SECURE_SSL_REDIRECT, bool)
        assert SECURE_PROXY_SSL_HEADER in (None, ("HTTP_X_FORWARDED_PROTO", "https"))

    def test_browser_xss_filter_setting_is_gone(self):
        """Django dropped SECURE_BROWSER_XSS_FILTER in 4.0; the setting is dead.

        The XSS auditor the setting controlled was removed from every browser
        in 2018, so keeping it only suggested protection that does not exist.
        """
        from pytigon.schserw.settings import infra

        assert not hasattr(infra, "SECURE_BROWSER_XSS_FILTER")

    def test_media_roots(self):
        from pytigon.schserw.settings.infra import (
            MEDIA_ROOT,
            MEDIA_ROOT_PROTECTED,
            MEDIA_URL,
            MEDIA_URL_PROTECTED,
        )

        assert isinstance(MEDIA_ROOT, str)
        assert isinstance(MEDIA_URL, str)

    def test_static_root_present(self):
        from pytigon.schserw.settings.base import STATIC_ROOT

        assert isinstance(STATIC_ROOT, str)
