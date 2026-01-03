import sys
import msvcrt
import msgpack

from node import Node
from helper import dict_to_node, node_to_dict

SAVED_OBJECT = 'saved_object/trie_object.msgpack'   # from createNewTrieFromTxt.py
SAVE_LOCATION = 'saved_object/trie_object.msgpack'
LIMIT_AUTO_COMPLETE = 10


with open(SAVE_LOCATION, "rb") as f:
    print("Loading trie...\n")
    # Strict map key false to allow int
    loaded_dict = msgpack.unpackb(f.read(), raw=False, strict_map_key=False)

root = dict_to_node(loaded_dict)


def run_traverse(node: Node, prefix="", limit=None):
    if isinstance(limit, int):
        limit = [limit]
    result = []
    if limit is not None and limit[0] <= 0:
        return result

    if node.is_end_of_word:
        if limit is not None:
            limit[0] -= 1
        result.append(prefix)
    for edgekey in node.edges.keys():
        if node.edges.get(edgekey):
            result.extend(run_traverse(
                node.edges[edgekey], prefix + chr(edgekey), limit))
    return result


def traverse(root: Node, user_input=""):
    if user_input == "":
        return run_traverse(root, user_input, LIMIT_AUTO_COMPLETE)
    curr = root
    for char in user_input:
        index = ord(char.lower())
        if not curr.edges.get(index):
            return []
        curr = curr.edges[index]
    return run_traverse(curr, user_input, LIMIT_AUTO_COMPLETE)

def delete(node: Node, to_del: str):
    if not node:
        return False
    if len(to_del) == 0:
        return False

    edge:Node = node.edges.get(ord(to_del[0]))
    if len(to_del) == 1:
        if edge and edge.is_end_of_word:
            edge.is_end_of_word = False
            return True
        else:
            return False
    else:
        found = delete(edge, to_del[1:])
        if found:
            # If the child node has no edges and is not end of another word, remove it
            if edge and not edge.is_end_of_word and len(edge.edges) == 0:
                del node.edges[ord(to_del[0])]
            return True
    

print("Press keys (Esc to exit, Enter to delete):")
print("Suggestions for ", end='', flush=True)
word = ""
prev_len = 100
was_deleted = False
while True:
    key = msvcrt.getwch()  # get a single Unicode character
    if key == '\x1b':      # Esc key
        if was_deleted:
            print("\nSaving changes to trie...")
            with open(SAVED_OBJECT, 'wb') as f:
                trie_dict = node_to_dict(root)
                packed = msgpack.packb(trie_dict, use_bin_type=True)
                f.write(packed)
            print("Changes saved.")
            print("\nExiting...")
        break
    elif key == '\x08':    # Backspace key
        word = word[:-1]
    elif key == '\r':   # Enter key
        deleted = delete(root, word)
        if deleted:
            print(f"\nDeleted word '{word}' from trie.\n")
            was_deleted = True
        else:
            print(f"\nWord '{word}' not found in trie.\n")
        word = ""
    else:
        word += key

    if word == "":
        sys.stdout.write('\r' + ' ' * prev_len + '\r')  # Clear line
        sys.stdout.write("Suggestions for : ")
        sys.stdout.flush()
        word = ""
        prev_len = 100
        continue
    
    suggestions = traverse(root, word)
    sys.stdout.write('\r' + ' ' * prev_len + '\r')  # Clear line

    OUT = f"Suggestions for '{word}': \t{suggestions}"
    prev_len = len(OUT) + 10
    sys.stdout.write(OUT)
    sys.stdout.flush()
