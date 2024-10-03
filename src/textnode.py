from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

def transform_link_node(node):
    return LeafNode("a", node.text, {"href": node.url})

def transform_image_node(node):
    return LeafNode("img", "", {"src": node.url, "alt": node.text})

transformation_map = {
    text_type_text: lambda node: LeafNode("", node.text),
    text_type_bold: lambda node: LeafNode("b", node.text),
    text_type_italic: lambda node: LeafNode("i", node.text),
    text_type_code: lambda node: LeafNode("code", node.text),
    text_type_link: transform_link_node,
    text_type_image: transform_image_node
}


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type in transformation_map:
        return transformation_map[text_node.text_type](text_node)
    else:
        raise Exception("Unknown TextNode type")
    
def extract_markdown_images(text):
    found_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return found_images

def extract_markdown_links(text):
    found_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return found_links