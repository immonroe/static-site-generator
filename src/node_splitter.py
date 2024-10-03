from textnode import TextNode
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