"""Additional tests for pytigon.schserw.schsys.templatetags.exfiltry module."""

import pytest


class TestExFiltryMore:
    def test_penultimate_elem_single(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import penultimate_elem

        assert penultimate_elem("a/b/c") == "b"

    def test_first_elem_with_sep(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import first_elem

        assert first_elem("a;b;c", ";") == "a"

    def test_last_elem_with_sep(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import last_elem

        assert last_elem("a;b;c", ";") == "c"

    def test_user_can_change_password(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import user_can_change_password

        user = type("User", (), {})()
        assert user_can_change_password(user) is True

    def test_get_or_tree_values(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import get_or_tree

        assert get_or_tree(1) == "gettree"
        assert get_or_tree(0) == "tree"
        assert get_or_tree("") == "tree"

    def test_append_get_param_with_question_mark(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import append_get_param

        result = append_get_param("/url/?a=1", "b=2")
        assert "b=2" in result

    def test_fdivide_by_zero(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import fdivide

        result = fdivide("10", "0")
        assert result == "" or result == 0.0

    def test_class_name_with_object(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import class_name

        obj = type("MyClass", (), {})()
        assert class_name(obj) == "MyClass"

    def test_filter_hasattr_dict(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import filter_hasattr

        assert filter_hasattr({}, "keys") is True

    def test_get_attr_nonexistent(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import get_attr

        assert get_attr("hello", "nonexistent") is None

    def test_model_can_have_children(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import model_can_have_children

        obj = type("Model", (), {})()
        assert model_can_have_children(obj) is True

    def test_model_can_have_children_false(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import model_can_have_children

        obj = type("Model", (), {"can_have_children": False})()
        assert model_can_have_children(obj) is False

    def test_bencode_bdecode_roundtrip(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import bencode, bdecode

        for text in ["hello", "world", "123", ""]:
            assert bdecode(bencode(text)) == text

    def test_one_line_block_multiple_spaces(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import one_line_block

        result = one_line_block("hello    world")
        assert "    " not in result or len(result) < len("hello    world")

    def test_clean_multiline(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import clean

        result = clean("line1\nline2\tline3")
        assert "\n" not in result
        assert "\t" not in result

    def test_append_str_none(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import append_str

        assert append_str("hello", None) == "hello"
        assert append_str("hello", "") == "hello"

    def test_remove_suffix_no_match(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import remove_suffix

        assert remove_suffix("hello", ".pdf") == "hello"

    def test_floatformat2_negative(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import floatformat2

        assert floatformat2("-3.14") == "-3.14"

    def test_to_console(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import to_console

        result = to_console("test")
        assert result == ""

    def test_filter_split_with_sep(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import filter_split

        assert filter_split("a,b,c", ",") == ["a", "b", "c"]

    def test_get_value_empty_list(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import get_value

        assert get_value([], "0") == ""

    def test_range_zero(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import _range

        assert _range("0") == []

    def test_eval_empty(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import _eval

        assert _eval("") == ""

    def test_amount_string(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import amount

        result = amount("1234")
        assert "1234" in result.replace(" ", "")

    def test_multiply_negative(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import multiply

        assert multiply("-2", "3") == -6

    def test_to_str_none(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import to_str

        assert to_str(None) == "" or to_str(None) == "None"

    def test_num2str_already_clean(self):
        from pytigon.schserw.schsys.templatetags.exfiltry import num2str

        result = num2str("42.5")
        assert "42.5" in result
