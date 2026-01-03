import msgpack
from node import Node
from helper import node_to_dict

TEXT_DATA_LOCATION = 'data/words.txt'
SAVE_LOCATION = 'saved_object/trie_object.msgpack'
root = Node()


def add_word(root: Node, word: str):
    curr = root
    for char in word:
        index = ord(char.lower())
        if not curr.edges.get(index):
            curr.edges[index] = Node()
        curr = curr.edges[index]
    curr.is_end_of_word = True

with open(TEXT_DATA_LOCATION, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for each in lines:
        line = each.strip()
        if line[0] == '#':
            continue
        add_word(root, line)

# Serialize the trie to a file using msgpack
with open(SAVE_LOCATION, 'wb') as f:
    trie_dict = node_to_dict(root)
    packed = msgpack.packb(trie_dict, use_bin_type=True)
    f.write(packed)

print("Trie has been created and saved.")
print("Cleaning up...")
