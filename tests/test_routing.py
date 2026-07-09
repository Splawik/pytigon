"""Tests for pytigon.schserw.routing module."""

from unittest.mock import patch

import pytest


class TestRouting:
    def test_lifespan_app_creation(self):
        from pytigon.schserw.routing import LifespanApp

        scope = {"type": "lifespan"}
        app = LifespanApp(scope)
        assert app.scope == scope

    def test_application_exists(self):
        from pytigon.schserw.routing import application

        assert application is not None
        assert hasattr(application, "__call__")
