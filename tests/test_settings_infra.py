"""Tests for pytigon.schserw.settings.infra module."""

import os
from unittest.mock import patch

import pytest


class TestSettingsInfra:
    def test_bootstrap_settings(self):
        from pytigon.schserw.settings.infra import (
            BOOTSTRAP5,
            BOOTSTRAP_ADMIN_SIDEBAR_MENU,
            BOOTSTRAP_BUTTON_SIZE_CLASS,
            BOOTSTRAP_TEMPLATE,
        )

        assert isinstance(BOOTSTRAP5, dict)
        assert "use_custom_controls" in BOOTSTRAP5
        assert BOOTSTRAP_ADMIN_SIDEBAR_MENU is True
        assert isinstance(BOOTSTRAP_BUTTON_SIZE_CLASS, str)
        assert isinstance(BOOTSTRAP_TEMPLATE, str)

    def test_three_level_menu(self):
        from pytigon.schserw.settings.infra import THREE_LEVEL_MENU

        assert THREE_LEVEL_MENU is False

    def test_asgi_application(self):
        from pytigon.schserw.settings.infra import ASGI_APPLICATION

        assert ASGI_APPLICATION == "pytigon.schserw.routing.application"

    def test_storages_configured(self):
        from pytigon.schserw.settings.infra import STORAGES

        assert "default" in STORAGES
        assert "staticfiles" in STORAGES
        assert "BACKEND" in STORAGES["default"]
        assert "BACKEND" in STORAGES["staticfiles"]

    def test_python_interpreter(self):
        from pytigon.schserw.settings.infra import PYTHON_CONSOLE, PYTHON_INTERPRETER

        import sys

        assert PYTHON_INTERPRETER == sys.executable
        assert PYTHON_CONSOLE == sys.executable

    def test_select2_settings(self):
        from pytigon.schserw.settings.infra import AUTO_RENDER_SELECT2_STATICS, SELECT2_THEME

        assert AUTO_RENDER_SELECT2_STATICS is False
        assert SELECT2_THEME == "bootstrap-5"

    def test_compress_storage(self):
        from pytigon.schserw.settings.infra import COMPRESS_STORAGE

        assert COMPRESS_STORAGE == "compressor.storage.GzipCompressorFileStorage"

    def test_default_file_storage_fs(self):
        from pytigon.schserw.settings.infra import DEFAULT_FILE_STORAGE_FS

        import importlib

        import pytigon.schserw.settings.infra as infra_mod

        importlib.reload(infra_mod)
        infra_mod.STATIC_FS = None
        infra_mod.ROOT_FS = None
        fs = infra_mod.DEFAULT_FILE_STORAGE_FS()
        assert fs is not None
        assert infra_mod.STATIC_FS is not None
        assert infra_mod.ROOT_FS is not None
