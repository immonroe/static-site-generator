import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leafnode_initialization(self):
        node = LeafNode("p", "Hello", {"class": "greeting"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "greeting"})

    def test_leafnode_to_html_with_tag(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leafnode_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click me!</a>')

    def test_leafnode_to_html_without_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leafnode_to_html_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_leafnode_repr(self):
        node = LeafNode("span", "Test", {"id": "test-span"})
        self.assertEqual(repr(node), "LeafNode(span, Test, {'id': 'test-span'})")

if __name__ == '__main__':
    unittest.main()