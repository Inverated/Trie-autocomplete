import msgpack
from node import Node

root = Node()


def add_word(root: Node, word: str):
    curr = root
    for char in word:
        index = ord(char.lower())
        if not curr.edges.get(index):
            curr.edges[index] = Node()
        curr = curr.edges[index]
    curr.is_end_of_word = True


def node_to_dict(node):
    """Recursively convert Node to dict for serialization."""
    return {
        "is_end_of_word": node.is_end_of_word,
        "edges": {char: node_to_dict(child) for char, child in node.edges.items()}
    }


with open('data/wiki-100k.txt', 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for each in lines:
        line = each.strip()
        if line[0] == '#':
            continue
        add_word(root, line)

# Serialize the trie to a file using msgpack
with open('saved_object/trie_object.msgpack', 'wb') as f:
    trie_dict = node_to_dict(root)
    packed = msgpack.packb(trie_dict, use_bin_type=True)
    f.write(packed)

print("Trie has been created and saved.")
