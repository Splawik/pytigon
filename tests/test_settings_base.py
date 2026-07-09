"""Tests for pytigon.schserw.settings.base module.

These tests verify the settings module provides expected values
in the test environment (which sets PYTIGON_DEBUG).
"""

import pytest


class TestSettingsBase:
    def test_gen_time_default(self):
        from pytigon.schserw.settings.base import GEN_TIME

        assert GEN_TIME == "0000.00.00 00:00:00"

    def test_use_tz(self):
        from pytigon.schserw.settings.base import USE_TZ

        assert USE_TZ is True

    def test_show_login_win(self):
        from pytigon.schserw.settings.base import SHOW_LOGIN_WIN

        assert SHOW_LOGIN_WIN is True

    def test_paths_present(self):
        from pytigon.schserw.settings.base import (
            DATA_PATH,
            LOG_PATH,
            PRJ_PATH,
            SERW_PATH,
            STATIC_ROOT,
            TEMP_PATH,
        )

        assert SERW_PATH
        assert DATA_PATH
        assert LOG_PATH
        assert TEMP_PATH
        assert PRJ_PATH
        assert STATIC_ROOT

    def test_media_settings(self):
        from pytigon.schserw.settings.base import MEDIA_ROOT, MEDIA_URL

        assert MEDIA_ROOT
        assert MEDIA_URL

    def test_secret_key_is_set(self):
        from pytigon.schserw.settings.base import SECRET_KEY

        assert SECRET_KEY is not None
        assert isinstance(SECRET_KEY, str)

    def test_language_settings(self):
        from pytigon.schserw.settings.base import LANGUAGE_CODE, LANGUAGES, TIME_ZONE

        assert LANGUAGE_CODE
        assert isinstance(LANGUAGES, (list, tuple))
        assert TIME_ZONE

    def test_database_has_default(self):
        from pytigon.schserw.settings.base import DATABASES

        assert isinstance(DATABASES, dict)

    def test_feature_flags_exist(self):
        from pytigon.schserw.settings.base import (
            ALLAUTH,
            COMPRESS_ENABLED,
            GRAPHQL,
            MAILER,
            PWA,
            REST,
            RULES_ENABLED,
        )

        assert isinstance(GRAPHQL, bool)
        assert isinstance(REST, bool)
        assert isinstance(RULES_ENABLED, bool)
        assert isinstance(MAILER, bool)
        assert isinstance(ALLAUTH, bool)
        assert isinstance(COMPRESS_ENABLED, bool)
        assert isinstance(PWA, bool)

    def test_date_input_formats(self):
        from pytigon.schserw.settings.base import DATE_INPUT_FORMATS

        assert "%Y-%m-%d" in DATE_INPUT_FORMATS
