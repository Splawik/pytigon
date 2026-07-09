"""Coverage tests for pytigon.schserw.schsys.templatetags.exsyntax module."""

import pytest


class TestExSyntaxCoverage:
    def test_functions_available(self):
        """Check that key functions are importable from exsyntax."""
        from pytigon.schserw.schsys.templatetags.exsyntax import (
            spec,
            editable_base,
            editable,
            new_row_base,
            new_row,
            include_wiki,
            markdown2html,
            icon,
            to_b64,
            wikify,
            register,
            get_row,
            button,
            field,
            show_context,
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
