# SynthReason v1.7 *ULTRA*
# Copyright 2024 George Wagenknecht
import random
from collections import defaultdict
import json
import math
size = 250
class Graph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self.aliases = {}
    def add_edge(self, u, v, w):
        weight = 1 
        self.graph[u][v][w] += weight
    def generate_text(self, start_word, text_length):
        if start_word not in self.graph:
            return "Word not found."
        current_word = start_word
        generated_text = [current_word]
        while len(generated_text) < text_length:
            next_nodes = self.graph[current_word]
            if not next_nodes:
                break
            next_words = []
            weights = []
            total_weights = {}
            for node, edges in next_nodes.items():
                total_weight = sum(edges.values())
                total_weights[node] = (1/total_weight)
            if sum(total_weights.values()) <= 0:
                break
            for node, total_weight in total_weights.items():
                if total_weight > 0:
                    next_words.append(node)
                    weights.append(len(next_words) * math.log2(1 / total_weight + 1))
            next_word = random.choices(next_words, weights=weights, k=1)[0]
            generated_text.append(next_word)
            current_word = next_word
        return ' '.join(generated_text)
    def load_graph(self, filename):
        with open(filename, 'r') as f:
            regular_dict = json.load(f)
        self.graph = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for u, v_dict in regular_dict.items():
            for v, w_dict in v_dict.items():
                for w, weight in w_dict.items():
                    self.graph[u][v][w] = weight
text_graph = Graph()
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
filename = "Compendium#" + str(random.randint(0, 10000000)) + ".txt"
random.shuffle(questions)
text_graph.load_graph('textgraph.json')
while(True):
    start_sequence = input("Start word:")
    generated_text = text_graph.generate_text(start_sequence,size)
    if generated_text:
        print("\n" + "Answering:", start_sequence, "\nAI:", generated_text, "\n\n")
        with open(filename, "a", encoding="utf8") as f:
            f.write("\n" +  "Answering: " + start_sequence + "\n" + generated_text + "\n")