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
            SECURE_BROWSER_XSS_FILTER,
            X_FRAME_OPTIONS,
            SECURE_REFERRER_POLICY,
        )

        assert isinstance(SECURE_BROWSER_XSS_FILTER, bool)
        assert isinstance(X_FRAME_OPTIONS, str)
        assert isinstance(SECURE_REFERRER_POLICY, str)

    def test_media_roots(self):
        from pytigon.schserw.settings.infra import MEDIA_ROOT, MEDIA_ROOT_PROTECTED
        from pytigon.schserw.settings.infra import MEDIA_URL, MEDIA_URL_PROTECTED

        assert isinstance(MEDIA_ROOT, str)
        assert isinstance(MEDIA_URL, str)

    def test_static_root_present(self):
        from pytigon.schserw.settings.base import STATIC_ROOT

        assert isinstance(STATIC_ROOT, str)
