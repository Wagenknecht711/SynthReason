# SynthReason v0.94 *ULTRA*
# Copyright 2024 George Wagenknecht
import random
from collections import defaultdict
import json
size = 250
class TextGraph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
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
            position = 0
            for node, edges in next_nodes.items():
                total_weight = sum(edges.values())
                if total_weight > 0:
                    next_words.append(node)
                    weights.append(total_weight*(position+1))
                    position += 1
            if not next_words:
                break
            next_word = random.choices(next_words, weights=weights, k=1)[0]
            generated_text.append(next_word)
            current_word = next_word
            text_length += 1
        return ' '.join(generated_text)
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
text_graph.load_graph('textgraph.json')
while(True):
    user_input = input("Start word:")
    generated_text = text_graph.generate_text(user_input)
    if generated_text:
        print("\n" + "Answering:", user_input, "\nAI:", generated_text, "\n\n")
        with open(filename, "a", encoding="utf8") as f:
            f.write("\n" +  "Answering: " + user_input + "\n" + generated_text + "\n")