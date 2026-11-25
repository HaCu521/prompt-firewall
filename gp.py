import json
import re
from random import choice

words=set()

for line in open("data/train.jsonl", encoding="utf-8"):
    if line.strip()== "":
        continue
    row=json.loads(line)
    if row["injected"]:
        payload_words = re.findall(r"[a-z]+", row["payload"].lower())
        canary_words = re.findall(r"[a-z]+", row["canary"].lower())
        for w in payload_words:
            if w not in canary_words:
                words.add(w)


class Node:
    def __init__(self, name, value, children):
        self.name = name          # "Word", "And" or "Or"
        self.value = value        # the word if name=="Word"
        self.children = children  # 0 children for "Word", 2 for "and"/"or"


def show(node, indent):
    if node.name == "Word":
        print("    " * indent + node.value)
    else:
        print("    " * indent + node.name)
        for child in node.children:
            show(child, indent + 1)



words=sorted(words)
print(words)

tree = Node("And", None, [
    Node("Word", choice(words), []),
    Node("Or", None, [
        Node("Word", choice(words), []),
        Node("Word", choice(words), [])
    ])
])
show(tree, 0)