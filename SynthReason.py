# SynthReason v1.41 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
import math
from collections import defaultdict
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
                total_weights[node] = total_weight
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
def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    filtered_words = [word for sentence in sentences for word in sentence.split() if user_words_set.intersection(sentence.split())]
    return filtered_words
def create_word_graph(text, user_words, n=3):
    words = text.split()
    word_graph = Graph()
    aliases = {}
    for i in range(len(words) - n + 1):
        ngram = tuple(words[i:i + n])
        if ngram in aliases:
            word_graph.add_edge(*aliases[ngram])
        else:
            aliases[ngram] = words[i:i + n]
            word_graph.add_edge(*ngram)
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
        user_input = input("USER: ").strip().lower()
        if not user_input:
            continue
        user_words = re.sub("\W+", " ", user_input).split()
        filtered_text = ' '.join(preprocess_text(text, user_words))
        word_graph = create_word_graph(filtered_text, user_input)
        generated_text = word_graph.generate_text(user_words[-1], size)
        if generated_text:
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break
