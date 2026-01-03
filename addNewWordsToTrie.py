import msgpack
from node import Node
from helper import dict_to_node, node_to_dict

TEXT_LOCATION = 'data/fakewordstotest.txt'
SAVED_OBJECT = 'saved_object/trie_object.msgpack'   # from createNewTrieFromTxt.py


with open(SAVED_OBJECT, "rb") as f:
    # Strict map key false to allow int
    loaded_dict = msgpack.unpackb(f.read(), raw=False, strict_map_key=False)

root = dict_to_node(loaded_dict)


def add_word(node: Node, word: str):
    curr = node
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
