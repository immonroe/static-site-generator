from textnode import TextNode, text_type_text, text_type_image, text_type_link, extract_markdown_images, extract_markdown_links
from htmlnode import HTMLNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        if node.text_type != "text":
            result.append(node)
        else:
            current_text = node.text
            while delimiter in current_text:
                start_index = current_text.index(delimiter)
                end_index = current_text.index(delimiter, start_index + len(delimiter))
                
                if end_index == -1:
                    raise ValueError(f"Unmatched delimiter '{delimiter}' found")

                if start_index > 0:
                    result.append(TextNode(current_text[:start_index], "text"))
                
                result.append(TextNode(current_text[start_index + len(delimiter):end_index], text_type))
                
                current_text = current_text[end_index + len(delimiter):]
            
            if current_text:
                result.append(TextNode(current_text, "text"))

    return result

def split_nodes_image(old_nodes):
    if not old_nodes or (len(old_nodes) == 1 and not old_nodes[0].text):
        return []

    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        
        current_text = node.text
        for i, image in enumerate(images):
            image_markdown = f"![{image[0]}]({image[1]})"
            parts = current_text.split(image_markdown, 1)
            
            if parts[0]:  # Text before the image
                new_nodes.append(TextNode(parts[0], text_type_text))
            
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            
            # Update current_text with the remaining part after the image
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        
        # Ensure to add remaining text, even if it's an empty string
        if current_text or len(images) > 0:
            new_nodes.append(TextNode(current_text, text_type_text))
    
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
        else:
            current_text = node.text
            for text, url in links:
                parts = current_text.split(f"[{text}]({url})", 1)
                if parts[0]:
                    new_nodes.append(TextNode(parts[0], text_type_text))
                new_nodes.append(TextNode(text, text_type_link, url))
                current_text = parts[1] if len(parts) > 1 else ""
            if current_text:
                new_nodes.append(TextNode(current_text, text_type_text))
    return new_nodes