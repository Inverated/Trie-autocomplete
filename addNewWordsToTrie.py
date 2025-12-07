import msgpack
from node import Node

TEXT_LOCATION = 'data/fakewordstotest.txt'
SAVED_OBJECT = 'saved_object/trie_object.msgpack'


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


with open(SAVED_OBJECT, "rb") as f:
    # Strict map key false to allow int
    loaded_dict = msgpack.unpackb(f.read(), raw=False, strict_map_key=False)

root = dict_to_node(loaded_dict)


def add_word(root: Node, word: str):
    curr = root
    for char in word:
        index = ord(char.lower())
        if not curr.edges.get(index):
            curr.edges[index] = Node()
        curr = curr.edges[index]
    curr.is_end_of_word = True


with open(TEXT_LOCATION, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for each in lines:
        line = each.strip()
        if line[0] == '#':
            continue
        add_word(root, line)

# Serialize the trie to a file using msgpack
with open(SAVED_OBJECT, 'wb') as f:
    trie_dict = node_to_dict(root)
    packed = msgpack.packb(trie_dict, use_bin_type=True)
    f.write(packed)

print("Trie has been updated and saved.")
print("Cleaning up...")
