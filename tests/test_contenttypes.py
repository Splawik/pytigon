"""Tests for pytigon.schserw.schsys.templatetags.contenttypes module."""

from unittest.mock import MagicMock, patch

import pytest


class TestContentTypes:
    def test_table_exists_true(self):
        with patch(
            "pytigon.schserw.schsys.templatetags.contenttypes.ContentType"
        ) as mock_ct:
            mock_ct.objects.get.return_value = MagicMock()
            from pytigon.schserw.schsys.templatetags.contenttypes import table_exists

            assert table_exists("auth_user") is True

    def test_table_exists_false(self):
        from django.core.exceptions import ObjectDoesNotExist

        with patch(
            "pytigon.schserw.schsys.templatetags.contenttypes.ContentType"
        ) as mock_ct:
            mock_ct.objects.get.side_effect = ObjectDoesNotExist()
            from pytigon.schserw.schsys.templatetags.contenttypes import table_exists

            assert table_exists("nonexistent") is False
