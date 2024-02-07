# SynthReason v0.9 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
from collections import defaultdict
import json
import os
size = 250
class TextGraph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    def add_edge(self, u, v, w, questions):
        weight = 1
        for question in questions:
            if u in question.split() or v in question.split() or w in question.split():
                weight += 1
        self.graph[u][v][w] += weight
    def generate_text(self, start_word):
        if start_word not in self.graph:
            return "Start word not found."
        current_word = start_word
        generated_text = [current_word]
        text_length = 1
        while text_length < size:
            next_nodes = self.graph[current_word]
            if not next_nodes:
                break
            next_words, weights = [], []
            for node, edges in next_nodes.items():
                total_weight = sum(edges.values())
                if total_weight > 0:
                    next_words.append(node)
                    weights.append(total_weight)
            if not next_words:
                break
            next_word = random.choices(next_words, weights=weights, k=1)[0]
            generated_text.append(next_word)
            current_word = next_word
            text_length += 1
        return ' '.join(generated_text)
    def preprocess_text(self, text, user_words):
        sentences = re.split(r'(?<=[.!?])\s+', text.lower())
        user_words_set = set(user_words)
        return [word for sentence in sentences for word in sentence.split() if user_words_set.intersection(sentence.split())]
    def create_from_text(self, text, questions, n=3):
        words = text.split()
        for i in range(len(words) - n + 1):
            ngram = tuple(words[i:i + n])
            self.add_edge(*ngram, questions)
    def save_graph(self, filename):
        current_graph_dict = {u: {v: dict(w_dict) for v, w_dict in v_dict.items()} for u, v_dict in self.graph.items()}
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
            for u, v_dict in current_graph_dict.items():
                for v, w_dict in v_dict.items():
                    for w, weight in w_dict.items():
                        existing_data.setdefault(u, {}).setdefault(v, {}).setdefault(w, 0)
                        existing_data[u][v][w] += weight
        else:
            existing_data = current_graph_dict
        with open(filename, 'w') as f:
            json.dump(existing_data, f)
    def load_graph(self, filename):
        with open(filename, 'r') as f:
            regular_dict = json.load(f)
        self.graph = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for u, v_dict in regular_dict.items():
            for v, w_dict in v_dict.items():
                for w, weight in w_dict.items():
                    self.graph[u][v][w] = weight
text_graph = TextGraph()
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
filename = "Compendium#" + str(random.randint(0, 10000000)) + ".txt"
random.shuffle(questions)
i = 1
for file in files:
    with open(file, encoding="UTF-8") as f:
        text = f.read()
    text_graph.create_from_text(text,questions)
    text_graph.save_graph('textgraph.json')
    text_graph.load_graph('textgraph.json')
    generated_text = text_graph.generate_text("the")
    user_input = ""
    print(i,"/", len( files))
    i+=1
    if generated_text:
        print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
        with open(filename, "a", encoding="utf8") as f:
            f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")