"""Coverage tests for pytigon.schserw.schsys.templatetags.exsyntax module."""

import pytest


class TestExSyntaxCoverage:
    def test_functions_available(self):
        """Check that key functions are importable from exsyntax."""
        from pytigon.schserw.schsys.templatetags.exsyntax import (
            button,
            editable,
            editable_base,
            field,
            get_row,
            icon,
            include_wiki,
            markdown2html,
            new_row,
            new_row_base,
            register,
            show_context,
            spec,
            to_b64,
            wikify,
        )
        assert callable(spec)
        assert callable(editable_base)
        assert callable(editable)
        assert callable(new_row_base)
        assert callable(new_row)
        assert callable(include_wiki)
        assert callable(markdown2html)
        assert callable(icon)
        assert callable(to_b64)
        assert callable(get_row)
        assert callable(button)
        assert callable(field)
        assert callable(show_context)
        assert register is not None
