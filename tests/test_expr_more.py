"""More tests for pytigon.schserw.schsys.templatetags.expr module."""

import pytest


class TestSafeEvalMore:
    def test_unary_negate(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("-5", {}) == -5
        assert _safe_eval("+5", {}) == 5

    def test_not_operator(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("not True", {}) is False
        assert _safe_eval("not False", {}) is True

    def test_in_operator(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("1 in [1, 2, 3]", {}) is True
        assert _safe_eval("4 in [1, 2, 3]", {}) is False

    def test_not_in_operator(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("4 not in [1, 2, 3]", {}) is True
        assert _safe_eval("1 not in [1, 2, 3]", {}) is False

    def test_floor_div(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("10 // 3", {}) == 3

    def test_chained_comparison(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("1 < 2 < 3", {}) is True
        assert _safe_eval("1 < 2 > 0", {}) is True

    def test_sorted_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("sorted([3, 1, 2])", {}) == [1, 2, 3]

    def test_bool_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("bool(1)", {}) is True
        assert _safe_eval("bool(0)", {}) is False

    def test_float_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("float('3.14')", {}) == 3.14

    def test_dict_literal(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        result = _safe_eval("{'a': 1, 'b': 2}", {})
        assert result == {"a": 1, "b": 2}

    def test_all_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("all([True, True])", {}) is True
        assert _safe_eval("all([True, False])", {}) is False

    def test_any_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("any([False, True])", {}) is True
        assert _safe_eval("any([False, False])", {}) is False

    def test_enumerate_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        result = _safe_eval("list(enumerate(['a', 'b']))", {})
        assert result == [(0, "a"), (1, "b")]

    def test_zip_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        result = _safe_eval("list(zip([1, 2], ['a', 'b']))", {})
        assert result == [(1, "a"), (2, "b")]

    def test_reversed_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        result = _safe_eval("list(reversed([1, 2, 3]))", {})
        assert result == [3, 2, 1]

    def test_range_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("list(range(3))", {}) == [0, 1, 2]

    def test_round_function(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("round(3.14159, 2)", {}) == 3.14

    def test_count_builtins_extended(self):
        from pytigon.schserw.schsys.templatetags.expr import _SAFE_BUILTINS

        assert _SAFE_BUILTINS.get("bin") is not None
        assert _SAFE_BUILTINS.get("hex") is not None
        assert _SAFE_BUILTINS.get("oct") is not None
        assert _SAFE_BUILTINS.get("chr") is not None
        assert _SAFE_BUILTINS.get("ord") is not None
        assert _SAFE_BUILTINS.get("divmod") is not None
        assert _SAFE_BUILTINS.get("pow") is not None
        assert _SAFE_BUILTINS.get("round") is not None
        assert _SAFE_BUILTINS.get("abs") is not None
