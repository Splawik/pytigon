"""Tests for pytigon.schserw.schsys.templatetags.exsyntax module."""

import pytest


class TestExSyntax:
    def test_spec_string_transformation(self):
        from pytigon.schserw.schsys.templatetags.exsyntax import spec

        result = spec("hello {name} [if x]")
        assert result == "hello {{name}} {%if x%}"

    def test_spec_preserves_normal_text(self):
        from pytigon.schserw.schsys.templatetags.exsyntax import spec

        result = spec("just normal text")
        assert result == "just normal text"

    def test_spec_brackets_only(self):
        from pytigon.schserw.schsys.templatetags.exsyntax import spec

        result = spec("{var1} {var2}")
        assert result == "{{var1}} {{var2}}"

    def test_spec_square_brackets_only(self):
        from pytigon.schserw.schsys.templatetags.exsyntax import spec

        result = spec("[block] [endblock]")
        assert result == "{%block%} {%endblock%}"

    def test_spec_mixed(self):
        from pytigon.schserw.schsys.templatetags.exsyntax import spec

        result = spec("{user.name} [if user.is_admin]admin[endif]")
        assert result == "{{user.name}} {%if user.is_admin%}admin{%endif%}"
