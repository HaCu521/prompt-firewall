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
        self.name = name          # "Word", "Near" or "Or"
        self.value = value        # the word if name=="Word"
        self.children = children  # 0 children for "Word",2 for "Near"/"Or"


def show(node, indent):
    if node.name == "Word":
        print("    " * indent + node.value)
    else:
        print("    " * indent + node.name)
        for child in node.children:
            show(child, indent + 1)


def to_regex(node):
    if node.name == "Word":
        return r"\b" + node.value + r"\b"
    elif node.name =="Or":
        return "(" + to_regex(node.children[0]) + "|" + to_regex(node.children[1]) + ")"
    elif node.name == "Near":
        return to_regex(node.children[0]) + ".{0,25}" + to_regex(node.children[1]) # 25 characters between two words/regex, 25characters are a couple of words

#baseline3 filter
def apply_tree(tree, text):
    regex =to_regex(tree)
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    kept_sentences = [s for s in sentences if not re.search(regex, s.lower())]
    if len(kept_sentences) == len(sentences):
        return text
    else:
        return " ".join(kept_sentences)

words=sorted(words)
print(words)

tree = Node("Near", None, [
    Node("Word", choice(words), []),
    Node("Or", None, [
        Node("Word", choice(words), []),
        Node("Word", choice(words), [])
    ])
])

show(tree, 0)
regex=to_regex(tree)
print(regex)
