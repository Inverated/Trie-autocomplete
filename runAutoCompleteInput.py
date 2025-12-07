import sys
import msvcrt
import msgpack

from node import Node


def dict_to_node(d):
    """Convert dict back to Node recursively."""
    node = Node()
    node.is_end_of_word = d["is_end_of_word"]
    node.edges = {char: dict_to_node(child)
                  for char, child in d["edges"].items()}
    return node


with open("saved_object/trie_object.msgpack", "rb") as f:
    print("Loading trie...")
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


def traverse(root: Node, user_input="", limit=10):
    if user_input == "":
        return run_traverse(root, user_input, limit)
    curr = root
    for char in user_input:
        index = ord(char.lower())
        if not curr.edges.get(index):
            return []
        curr = curr.edges[index]
    return run_traverse(curr, user_input, limit)


print("Press keys (Esc to exit):")
print("Suggestions for ", end='', flush=True)
word = ""
prev_len = 100
while True:
    key = msvcrt.getwch()  # get a single Unicode character
    if key == '\x1b':      # Esc key
        print("\nExiting...")
        break
    elif key == '\x08':    # Backspace key
        word = word[:-1]
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

    OUT = f"Suggestions for '{word}': {suggestions}"
    prev_len = len(OUT)
    sys.stdout.write(OUT)
    sys.stdout.flush()
