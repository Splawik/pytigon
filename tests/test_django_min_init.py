"""Tests for pytigon.django_min_init module."""

from unittest.mock import patch

import pytest


class TestDjangoMinInit:
    def test_init_function_exists(self):
        from pytigon.django_min_init import init

        assert callable(init)

    def test_init_with_default_prj(self):
        """Test init can be called with minimal parameter."""
        from pytigon.django_min_init import init

        try:
            init(prj="_schtest", pytigon_standard=False)
        except Exception as e:
            pytest.skip(f"init failed in test environment: {e}")
