import unittest
from node_splitter import split_nodes_delimiter
from htmlnode import LeafNode
from textnode import text_node_to_html_node
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_text_node_to_html_text(self):
        text_node = TextNode("This is a text", text_type_text)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("", "This is a text")
        self.assertEqual(html_node, expected_html_node)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is text with a `code block` word", "text")
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is text with a ")
        self.assertEqual(result[1].text, "code block")
        self.assertEqual(result[1].text_type, "code")
        self.assertEqual(result[2].text, " word")

    def test_multiple_delimiters(self):
        node = TextNode("**Bold** and *italic* text", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        result = split_nodes_delimiter(result, "*", "italic")
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text_type, "bold")
        self.assertEqual(result[2].text_type, "italic")

if __name__ == "__main__":
    unittest.main()
