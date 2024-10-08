import re
from htmlnode import HTMLNode
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text):
    # Initialize an empty list to store the child nodes
    children = []
    
    # Process the text for inline markdown
    # You'll use your previously created functions here
    # For example:
    # - split_nodes_delimiter
    # - extract_markdown_links
    # - text_node_to_html_node
    
    # ... Your processing logic here ...
    
    # Return the list of child nodes
    return children

def markdown_to_blocks(markdown):
    lines = markdown.split('\n')

    blocks = []
    current_block = []

    for line in lines:
        if line.strip() == '':
            if current_block:
                blocks.append('\n'.join(current_block))
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append('\n'.join(current_block))

    blocks = [block.strip() for block in blocks if block.strip()]

    return blocks

def block_to_block_type(block: str) -> str:
    lines = block.split('\n')
    first_line = lines[0].strip()
    
    if first_line.startswith('#'):
        if ' ' in first_line and first_line.index(' ') <= 6:
            return 'heading'
    elif block.startswith('```') and block.endswith('```'):
        return 'code'
    elif all(line.strip().startswith('>') for line in lines):
        return 'quote'
    elif all(line.strip().startswith(('*', '-')) for line in lines):
        return 'unordered_list'
    elif all(line.strip()[0].isdigit() and line.strip()[1:].startswith('. ') for line in lines):
        return 'ordered_list'
    
    return 'paragraph'

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "paragraph":
            node = HTMLNode(tag="p")
            node.children = text_to_children(block)
        elif block_type == "heading":
            level = block.count('#')
            node = HTMLNode(tag=f"h{level}")
            node.children = text_to_children(block.lstrip('#').strip())
    # ... handle other block types similarly
        elif block_type == "code":
            # Create code block node
        elif block_type == "quote":
            # Create code block node
        elif block_type == "unordered_list":
            # Create code block node
        elif block_type == "ordered_list":
            # Create code block node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches
