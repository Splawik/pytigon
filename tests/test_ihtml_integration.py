"""Integration tests for the iHTML pipeline and Django template rendering.

The iHTML source is first compiled to (structural) HTML with
``ihtml_to_html``, then the ``{var}``/``[if]`` sugar is turned into Django
template syntax with ``spec``, and finally the result is rendered through the
Django template engine with a real context.
"""

import os
import textwrap

from django.template import Context, Engine

from pytigon.schserw.schsys.templatetags.exsyntax import spec
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html


def _compile_and_render(ihtml_src, context=None):
    """Compile iHTML -> structural HTML -> Django syntax, then render."""
    html = ihtml_to_html(None, input_str=ihtml_src)
    engine = Engine()
    return html, engine.from_string(spec(html)).render(Context(context or {}))


# ---------------------------------------------------------------------------
# iHTML -> structural HTML conversion
# ---------------------------------------------------------------------------


class TestIhtmlToHtml:
    def test_basic_elements(self):
        html = ihtml_to_html(
            None,
            input_str=textwrap.dedent(
                """\
                div
                    p
                        Hello World
                """
            ),
        )
        assert "<div" in html
        assert "<p" in html

    def test_text_content_present(self):
        html = ihtml_to_html(
            None,
            input_str="div\n    p\n        Hello World",
        )
        assert "Hello World" in html


# ---------------------------------------------------------------------------
# spec(): iHTML sugar -> Django template syntax
# ---------------------------------------------------------------------------


class TestSpec:
    def test_variable_conversion(self):
        assert spec("{name}") == "{{name}}"

    def test_block_conversion(self):
        assert spec("[if x]") == "{%if x%}"
        assert spec("[endif]") == "{%endif%}"

    def test_for_conversion(self):
        assert spec("[for i in items]") == "{%for i in items%}"
        assert spec("[endfor]") == "{%endfor%}"

    def test_mixed(self):
        result = spec("{user.name} [if user]yes[endif]")
        assert result == "{{user.name}} {%if user%}yes{%endif%}"


# ---------------------------------------------------------------------------
# Full pipeline: iHTML + spec + Django render
# ---------------------------------------------------------------------------


class TestPipeline:
    def test_variable_renders(self):
        html, out = _compile_and_render(
            "div\n    p\n        {greeting}",
            {"greeting": "hi"},
        )
        assert "hi" in out

    def test_if_true_false(self):
        src = "div\n    [if show]\n        visible\n    [endif]"
        _, out_true = _compile_and_render(src, {"show": True})
        assert "visible" in out_true
        _, out_false = _compile_and_render(src, {"show": False})
        assert "visible" not in out_false

    def test_for_loop(self):
        src = "ul\n    [for item in items]\n        li\n            {item}\n    [endfor]\n"
        _, out = _compile_and_render(src, {"items": ["a", "b", "c"]})
        assert "a" in out
        assert "b" in out
        assert "c" in out

    def test_autoescape_applies(self):
        _, out = _compile_and_render(
            "div\n    {value}",
            {"value": "<script>alert('x')</script>"},
        )
        assert "&lt;script&gt;" in out
        assert "<script>alert" not in out


# ---------------------------------------------------------------------------
# FSLoader-style compilation of a real .ihtml file
# ---------------------------------------------------------------------------


class TestFSCompilation:
    def test_compile_and_write_ihtml(self, tmp_path, monkeypatch):
        from django.conf import settings

        from pytigon_lib.schdjangoext.python_style_template_loader import (
            _compile_and_write_ihtml,
        )

        src_ihtml = str(tmp_path / "templates_src" / "page.ihtml")
        out_html = str(tmp_path / "templates" / "page.html")
        monkeypatch.setattr(settings, "LANGUAGES", [("en", "English")])

        _compile_and_write_ihtml(
            src_ihtml,
            out_html,
            source="div\n    p\n        {title}\n",
        )

        assert os.path.exists(out_html)
        content = open(out_html, encoding="utf-8").read()
        assert "<div" in content
