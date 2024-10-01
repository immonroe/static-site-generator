import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"class": "my-class", "id": "my-id", "href": "https://example.com"})
        expected = ' class="my-class" id="my-id" href="https://example.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode(tag="a", value="Click me!", props={"href": "https://example.com"})
        expected = "HTMLNode(tag='a', value='Click me!', children=None, props={'href': 'https://example.com'})"
        self.assertEqual(repr(node), expected)

if __name__ == '__main__':
    unittest.main()