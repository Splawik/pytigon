"""Tests for pytigon.schserw.schsys.urls module."""

import pytest


class TestSchSysUrls:
    def test_urlpatterns_imports(self):
        from pytigon.schserw.schsys.urls import urlpatterns

        assert isinstance(urlpatterns, list)

    def test_urlpatterns_not_empty(self):
        from pytigon.schserw.schsys.urls import urlpatterns

        assert len(urlpatterns) > 0
