import json
import re

MAILS = []
for line in open("data/train.jsonl", encoding="utf-8"):
    if line.strip() == "":
        continue
    row = json.loads(line)
    MAILS.append({"text": row["text"], "payload": row["payload"], "clean": row["clean"]})

#baseline 2 test
def apply_filter(words, text):
    """splits text into sentences and removes sentences containing a word"""
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    kept_sentences = [s for s in sentences if not any(w in s.lower() for w in words)]
    if len(kept_sentences) == len(sentences):
        return text
    else:
        return " ".join(kept_sentences)

def fitness(words):
    """Returns filter value"""
    attacked = [m for m in MAILS if m["payload"]]

    removed = 0    # attacks that are gone
    cleaned = 0    # emails in which the filter deleted anything
    for m in MAILS:
        filtered = apply_filter(words, m["text"])
        if filtered != m["text"]:
            cleaned += 1

        if m["payload"] and filtered == m["clean"]:
            removed += 1

    recall = removed / len(attacked)
    if cleaned: #cleaned cannot be 0
        precision = removed / cleaned
    else:
        precision=0

    if precision + recall == 0:
        return 0.0

    BETA = 2

    # same fitness as paper:Data-Driven Regular Expressions Evolution for Medical Text Classification Using Genetic Programming
    fitness_score = (1 + BETA ** 2) * precision * recall / (BETA ** 2 * precision + recall)
    return fitness_score

if __name__ == "__main__":
    words = ["your response", "output only", "test marker"]
    print("fitness : ", round(fitness(words), 2))