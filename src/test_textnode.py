import unittest
from node_splitter import (
    split_nodes_delimiter, 
    split_nodes_image, 
    split_nodes_link)
from htmlnode import LeafNode
from textnode import (
    text_node_to_html_node, 
    extract_markdown_images, 
    extract_markdown_links)
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

class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://example.com/image.jpg) and another ![second image](https://example.com/image2.png)"
        expected = [("image", "https://example.com/image.jpg"), ("second image", "https://example.com/image2.png")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://example.com) and [another link](https://example.com/page)"
        expected = [("link", "https://example.com"), ("another link", "https://example.com/page")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_mixed(self):
        text = "Text with a ![image](https://example.com/image.jpg) and a [link](https://example.com)"
        self.assertEqual(extract_markdown_images(text), [("image", "https://example.com/image.jpg")])
        self.assertEqual(extract_markdown_links(text), [("link", "https://example.com")])

    def test_extract_markdown_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_links(""), [])
    
class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode("This is an ![image](https://example.com/image.jpg) in text", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is an ")
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].url, "https://example.com/image.jpg")
        self.assertEqual(result[2].text, " in text")

    def test_split_multiple_images(self):
        node = TextNode("![First](https://example.com/1.jpg) and ![Second](https://example.com/2.jpg)", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "First")
        self.assertEqual(result[0].url, "https://example.com/1.jpg")
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[2].text, "Second")
        self.assertEqual(result[2].url, "https://example.com/2.jpg")

class TestSplitNodesImage(unittest.TestCase):
    def test_split_single_image(self):
        node = TextNode("This is an ![image](https://example.com/image.jpg) in text", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is an ")
        self.assertEqual(result[1].text, "image")
        self.assertEqual(result[1].url, "https://example.com/image.jpg")
        self.assertEqual(result[2].text, " in text")

    def test_split_multiple_images(self):
        node = TextNode("![First](first.png) and ![Second](second.png)", text_type_text)
        result = split_nodes_image([node])
        
        # Debug print statements
        print("\nResult nodes:")
        for i, n in enumerate(result):
            print(f"{i}: {n.text} ({n.text_type})")
        
        # Original assertions
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "First")
        self.assertEqual(result[0].text_type, text_type_image)
        self.assertEqual(result[0].url, "first.png")
        self.assertEqual(result[1].text, " and ")
        self.assertEqual(result[1].text_type, text_type_text)
        self.assertEqual(result[2].text, "Second")
        self.assertEqual(result[2].text_type, text_type_image)
        self.assertEqual(result[2].url, "second.png")
        self.assertEqual(result[3].text, "")
        self.assertEqual(result[3].text_type, text_type_text)

    def test_no_links(self):
        node = TextNode("This is text with no links", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is text with no links")

    def test_multiple_nodes(self):
        node1 = TextNode("Start [link](https://example.com) end", text_type_text)
        node2 = TextNode("No link here", text_type_text)
        result = split_nodes_link([node1, node2])
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].url, "https://example.com")
        self.assertEqual(result[2].text, " end")
        self.assertEqual(result[3].text, "No link here")

    def test_empty_node(self):
        node = TextNode("", text_type_text)
        result = split_nodes_image([node])
        self.assertEqual(len(result), 0)

    def test_link_at_start_and_end(self):
        node = TextNode("[Start](https://start.com)middle[End](https://end.com)", text_type_text)
        result = split_nodes_link([node])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Start")
        self.assertEqual(result[0].url, "https://start.com")
        self.assertEqual(result[1].text, "middle")
        self.assertEqual(result[2].text, "End")
        self.assertEqual(result[2].url, "https://end.com")

if __name__ == "__main__":
    unittest.main()
