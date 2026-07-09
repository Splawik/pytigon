"""Tests for pytigon.schserw.schsys.templatetags.expr module (safe eval)."""

import pytest


class TestSafeEval:
    def test_safe_eval_literals(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("42", {}) == 42
        assert _safe_eval("3.14", {}) == 3.14
        assert _safe_eval("True", {}) is True
        assert _safe_eval("False", {}) is False
        assert _safe_eval("None", {}) is None
        assert _safe_eval('"hello"', {}) == "hello"

    def test_safe_eval_arithmetic(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("1 + 2", {}) == 3
        assert _safe_eval("10 - 3", {}) == 7
        assert _safe_eval("4 * 5", {}) == 20
        assert _safe_eval("10 / 3", {}) == pytest.approx(3.33, 0.1)
        assert _safe_eval("10 // 3", {}) == 3
        assert _safe_eval("10 % 3", {}) == 1
        assert _safe_eval("2 ** 3", {}) == 8

    def test_safe_eval_comparisons(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("1 == 1", {}) is True
        assert _safe_eval("1 != 2", {}) is True
        assert _safe_eval("1 < 2", {}) is True
        assert _safe_eval("2 > 1", {}) is True
        assert _safe_eval("1 <= 1", {}) is True
        assert _safe_eval("2 >= 1", {}) is True

    def test_safe_eval_bool_ops(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("True and True", {}) is True
        assert _safe_eval("True and False", {}) is False
        assert _safe_eval("True or False", {}) is True
        assert _safe_eval("False or False", {}) is False

    def test_safe_eval_variables(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("x + y", {"x": 10, "y": 20}) == 30
        assert _safe_eval("x > y", {"x": 10, "y": 5}) is True

    def test_safe_eval_if_expression(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("1 if True else 2", {}) == 1
        assert _safe_eval("1 if False else 2", {}) == 2

    def test_safe_eval_builtins(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        assert _safe_eval("len('abc')", {}) == 3
        assert _safe_eval("str(42)", {}) == "42"
        assert _safe_eval("int('42')", {}) == 42
        assert _safe_eval("abs(-5)", {}) == 5
        assert _safe_eval("min(1, 2, 3)", {}) == 1
        assert _safe_eval("max(1, 2, 3)", {}) == 3
        assert _safe_eval("sum([1, 2, 3])", {}) == 6

    def test_safe_eval_undefined_name_raises(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        with pytest.raises((NameError, ValueError)):
            _safe_eval("undefined_var", {})

    def test_safe_eval_forbidden_builtin_raises(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        with pytest.raises((NameError, ValueError)):
            _safe_eval("__import__('os')", {})

    def test_safe_eval_join_string(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        result = _safe_eval('",".join(["a", "b", "c"])', {})
        assert result == "a,b,c"

    def test_safe_eval_subscript(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        result = _safe_eval("data['key']", {"data": {"key": "value"}})
        assert result == "value"

    def test_safe_eval_list_subscript(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        result = _safe_eval("data[1]", {"data": [10, 20, 30]})
        assert result == 20

    def test_safe_eval_attribute_access(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        result = _safe_eval('"hello".upper()', {})
        assert result == "HELLO"

        result = _safe_eval('"HELLO".lower()', {})
        assert result == "hello"

    def test_safe_eval_list_append(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        data = [1, 2]
        _safe_eval("data.append(3)", {"data": data})
        assert data == [1, 2, 3]

    def test_safe_builtins_contains_expected(self):
        from pytigon.schserw.schsys.templatetags.expr import _SAFE_BUILTINS

        assert "len" in _SAFE_BUILTINS
        assert "str" in _SAFE_BUILTINS
        assert "int" in _SAFE_BUILTINS
        assert "list" in _SAFE_BUILTINS
        assert "dict" in _SAFE_BUILTINS
        assert "True" in _SAFE_BUILTINS
        assert "False" in _SAFE_BUILTINS
        assert "None" in _SAFE_BUILTINS

    def test_safe_ops_contains_expected(self):
        from pytigon.schserw.schsys.templatetags.expr import _SAFE_OPS

        import ast

        assert ast.Add in _SAFE_OPS
        assert ast.Sub in _SAFE_OPS
        assert ast.Mult in _SAFE_OPS

    def test_is_safe_attribute_allows_lower(self):
        from pytigon.schserw.schsys.templatetags.expr import _is_safe_attribute

        assert _is_safe_attribute("hello", "lower") is True

    def test_is_safe_attribute_blocks_private(self):
        from pytigon.schserw.schsys.templatetags.expr import _is_safe_attribute

        with pytest.raises(ValueError, match="forbidden"):
            _is_safe_attribute("hello", "__class__")

    def test_is_safe_attribute_blocks_unknown(self):
        from pytigon.schserw.schsys.templatetags.expr import _is_safe_attribute

        with pytest.raises(ValueError, match="not allowed"):
            _is_safe_attribute("hello", "xyz_unknown_method")

    def test_safe_eval_list_pop(self):
        from pytigon.schserw.schsys.templatetags.expr import _safe_eval

        data = [1, 2, 3]
        result = _safe_eval("data.pop()", {"data": data})
        assert result == 3
        assert data == [1, 2]
