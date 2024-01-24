# SynthReason v0.1 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
from collections import defaultdict
import math
class Graph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self.aliases = {}
    def add_edge(self, u, v, w,text):
        self.graph[u][v][w] += max(1.0,len(u) - len(v) *len(w))
    def generate_text(self, start_word, size=250):
        if start_word not in self.graph:
            return "Start word not found."
        current_word = start_word
        generated_text = [current_word]
        while len(generated_text) < size:
            next_nodes = self.graph[current_word]
            if not next_nodes:
                break
            next_words = []
            weights = []
            for node, edges in next_nodes.items():
                for edge, weight in edges.items():
                    next_words.append(node)
                    weights.append(weight)
            next_word = random.choices(next_words, weights=weights, k=1)[0]
            generated_text.append(next_word)
            current_word = next_word
        return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    filtered_words = [word for sentence in sentences for word in sentence.split() if user_words_set.intersection(sentence.split())]
    return filtered_words
def create_word_graph(text):
    words = text.split()
    word_graph = Graph()
    aliases = {}
    for i, word in enumerate(words):
        if i < len(words)-3:
            if words[i] in aliases and words[i + 1] in aliases and words[i + 2] in aliases:
                word_graph.add_edge(aliases[words[i]], aliases[words[i + 1]], aliases[words[i + 2]],words)
            else:
                aliases[words[i]] = word
                word_graph.add_edge(words[i], words[i + 1], words[i + 2],words)
    return word_graph
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
filename = "Compendium#" + str(random.randint(0, 10000000)) + ".txt"
random.shuffle(questions)
for question in questions:
    random.shuffle(files)
    for file in files:
        with open(file, encoding="UTF-8") as f:
            text = f.read()
        user_input = question.strip().lower()
        if not user_input:
            continue
        user_words = re.sub("\W+", " ", user_input).split()
        filtered_text = ' '.join(preprocess_text(text, user_words))
        word_graph = create_word_graph(filtered_text)
        generated_text = word_graph.generate_text(user_words[0])
        if generated_text:
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break