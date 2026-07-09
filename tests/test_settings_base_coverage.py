"""Test that settings.base module imports and has expected types."""

import pytest


class TestSettingsBaseCoverage:
    def test_all_base_settings_types(self):
        import pytigon.schserw.settings.base as base_mod

        vars_to_check = [
            "BASE_PRJ_NAME",
            "DATA_PATH",
            "DATE_INPUT_FORMATS",
            "DATABASES",
            "DB_DEBUG",
            "DEBUG",
            "GEN_TIME",
            "LANGUAGE_CODE",
            "LANGUAGES",
            "LOG_PATH",
            "MEDIA_ROOT",
            "MEDIA_ROOT_PROTECTED",
            "MEDIA_URL",
            "MEDIA_URL_PROTECTED",
            "PLATFORM_TYPE",
            "PRJ_PATH",
            "PRJ_PATH_ALT",
            "PRODUCTION_VERSION",
            "PUBLIC",
            "SCRIPT_MODE",
            "SECRET_KEY",
            "SERW_PATH",
            "SHOW_LOGIN_WIN",
            "STATIC_ROOT",
            "STATICFILES_DIRS",
            "TEMP_PATH",
            "TIME_ZONE",
            "USE_TZ",
            "URL_ROOT_FOLDER",
            "GRAPHQL",
            "REST",
            "RULES_ENABLED",
            "MAILER",
            "ALLAUTH",
            "COMPRESS_ENABLED",
            "PWA",
            "PYTIGON_PATH",
        ]
        for var in vars_to_check:
            val = getattr(base_mod, var, None)
            assert val is not None, f"{var} is None"
