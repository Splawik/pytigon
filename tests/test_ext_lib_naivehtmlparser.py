"""
Pytest tests for pytigon.ext_lib.naivehtmlparser module.
"""

import pytest
from xml.etree import ElementTree
from pytigon.ext_lib.naivehtmlparser import NaiveHTMLParser


class TestNaiveHTMLParser:
    def test_initialization(self):
        """Test NaiveHTMLParser initializes with None root and empty tree."""
        parser = NaiveHTMLParser()
        assert parser.root is None
        assert parser.tree == []

    def test_feed_returns_root(self):
        """Test feed() parses HTML and returns root element."""
        html = "<html><head><title>Test</title></head><body>Content</body></html>"
        parser = NaiveHTMLParser()
        root = parser.feed(html)
        parser.close()

        assert root is not None
        assert root.tag == "html"
        assert parser.get_root_element() is root

    def test_parse_simple_structure(self):
        """Test parsing a simple HTML structure."""
        html = """
        <html>
          <head>
            <title>GitHub</title>
          </head>
          <body>
            <a href="https://github.com">GitHub</a>
          </body>
        </html>
        """
        parser = NaiveHTMLParser()
        root = parser.feed(html)
        parser.close()

        # Find title
        title = root.find("head/title")
        assert title is not None
        assert title.text.strip() == "GitHub"

        # Find anchor
        anchor = root.find(".//a")
        assert anchor is not None
        assert anchor.get("href") == "https://github.com"
        assert anchor.text.strip() == "GitHub"

    def test_parse_empty_html(self):
        """Test parsing empty HTML returns root."""
        html = ""
        parser = NaiveHTMLParser()
        root = parser.feed(html)
        parser.close()
        # Empty input gives None root
        assert root is None

    def test_parse_self_closing_tags(self):
        """Test parsing self-closing tags like <br/>."""
        html = "<div><br/><hr/></div>"
        parser = NaiveHTMLParser()
        root = parser.feed(html)
        parser.close()

        assert root is not None
        assert root.tag == "div"
        # Self-closing tags are treated as start+end
        children = list(root)
        assert len(children) == 2
        assert children[0].tag == "br"
        assert children[1].tag == "hr"

    def test_parse_tags_with_attributes(self):
        """Test parsing tags with attributes are properly handled."""
        html = '<div class="container" id="main"><p>Text</p></div>'
        parser = NaiveHTMLParser()
        root = parser.feed(html)
        parser.close()

        assert root is not None
        assert root.tag == "div"
        assert root.get("class") == "container"
        assert root.get("id") == "main"

    def test_filter_empty_attributes(self):
        """Test that empty or None attributes are filtered out."""
        html = "<div class='' id='main'><p>Text</p></div>"
        parser = NaiveHTMLParser()
        root = parser.feed(html)
        parser.close()

        assert root is not None
        # Empty attributes should be filtered
        assert root.get("class") is None
        assert root.get("id") == "main"

    def test_get_root_element_before_feed(self):
        """Test get_root_element returns None before parsing."""
        parser = NaiveHTMLParser()
        assert parser.get_root_element() is None

    def test_handle_data_appends_text(self):
        """Test that handle_data appends text properly."""
        html = "<p>Hello World</p>"
        parser = NaiveHTMLParser()
        root = parser.feed(html)
        parser.close()

        assert root is not None
        assert root.tag == "p"
        assert root.text == "Hello World"

    def test_nested_elements_text_handling(self):
        """Test text handling with nested elements."""
        html = "<div>Before<span>Inside</span>After</div>"
        parser = NaiveHTMLParser()
        root = parser.feed(html)
        parser.close()

        assert root is not None
        assert root.tag == "div"
        # The text "Before" and "After" should be in div's text and tail
        assert root.text is not None
        child = list(root)[0]
        assert child.tag == "span"
        assert child.text == "Inside"
