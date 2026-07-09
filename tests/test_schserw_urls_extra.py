"""Tests for pytigon.schserw.urls module."""

from unittest.mock import MagicMock, patch

import pytest


class TestUrls:
    def test_urlpatterns_is_list(self):
        from pytigon.schserw.urls import urlpatterns

        assert isinstance(urlpatterns, list)
        assert len(urlpatterns) > 0
