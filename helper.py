from node import Node

def dict_to_node(d):
    """Convert dict back to Node recursively."""
    node = Node()
    node.is_end_of_word = d["is_end_of_word"]
    node.edges = {char: dict_to_node(child)
                  for char, child in d["edges"].items()}
    return node

def node_to_dict(node):
    """Recursively convert Node to dict for serialization."""
    return {
        "is_end_of_word": node.is_end_of_word,
        "edges": {char: node_to_dict(child) for char, child in node.edges.items()}
    }