"""Extended tests for pytigon.ext_lib.naivehtmlparser module."""

import pytest


class TestNaiveHTMLParser:
    def test_parse_simple_html(self):
        from pytigon.ext_lib.naivehtmlparser import NaiveHTMLParser

        parser = NaiveHTMLParser()
        root = parser.feed("<html><body><p>Hello</p></body></html>")
        assert root is not None
        assert root.tag == "html"

    def test_parse_with_attributes(self):
        from pytigon.ext_lib.naivehtmlparser import NaiveHTMLParser

        parser = NaiveHTMLParser()
        root = parser.feed('<div class="test" id="main">content</div>')
        assert root.tag == "div"
        assert root.attrib.get("class") == "test"
        assert root.attrib.get("id") == "main"
        assert root.text == "content"

    def test_parse_self_closing_tag(self):
        from pytigon.ext_lib.naivehtmlparser import NaiveHTMLParser

        parser = NaiveHTMLParser()
        root = parser.feed("<div><br/><span>text</span></div>")
        assert root.tag == "div"
        children = list(root)
        assert len(children) == 2

    def test_parse_nested(self):
        from pytigon.ext_lib.naivehtmlparser import NaiveHTMLParser

        parser = NaiveHTMLParser()
        root = parser.feed("<ul><li>A</li><li>B</li></ul>")
        assert root.tag == "ul"
        children = list(root)
        assert len(children) == 2
        assert children[0].text == "A"
        assert children[1].text == "B"

    def test_get_root_element(self):
        from pytigon.ext_lib.naivehtmlparser import NaiveHTMLParser

        parser = NaiveHTMLParser()
        root = parser.feed("<root/>")
        assert parser.get_root_element() is root

    def test_text_accumulation(self):
        from pytigon.ext_lib.naivehtmlparser import NaiveHTMLParser

        parser = NaiveHTMLParser()
        root = parser.feed("<p>Hello World</p>")
        assert root.text == "Hello World"

    def test_empty_element(self):
        from pytigon.ext_lib.naivehtmlparser import NaiveHTMLParser

        parser = NaiveHTMLParser()
        root = parser.feed("<div></div>")
        assert root.tag == "div"
        assert root.text is None or root.text == ""
