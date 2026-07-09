"""Tests for pytigon.schserw.schsys.templatetags.defexfiltry module."""

import pytest


class TestDefExFiltry:
    def test_translate_english(self):
        from pytigon.schserw.schsys.templatetags.defexfiltry import translate

        assert translate("template.html", "en") == "template.html"

    def test_translate_polish(self):
        from pytigon.schserw.schsys.templatetags.defexfiltry import translate

        assert translate("template.html", "pl") == "template_pl.html"

    def test_translate_empty_lang(self):
        from pytigon.schserw.schsys.templatetags.defexfiltry import translate

        assert translate("template.html", "") == "template.html"

    def test_translate_none_string_raises(self):
        from pytigon.schserw.schsys.templatetags.defexfiltry import translate

        with pytest.raises(ValueError, match="must be strings"):
            translate(123, "en")
