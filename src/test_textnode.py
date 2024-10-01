import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_property(self):
        node = TextNode("Hello, world!", "bold")
        self.assertEqual(node.text, "Hello, world!")

    def test_text_type_property(self):
        node = TextNode("Hello, world!", "italic")
        self.assertEqual(node.text_type, "italic")

    def test_url_property_none(self):
        node = TextNode("Hello, world!", "bold")
        self.assertIsNone(node.url)

    def test_inequality(self):
        node1 = TextNode("Hello, world!", "bold")
        node2 = TextNode("Hello, world!", "italic")
        self.assertNotEqual(node1, node2)

    def test_url_inequality(self):
        node1 = TextNode("Hello, world!", "bold", "https://example.com")
        node2 = TextNode("Hello, world!", "bold")
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()