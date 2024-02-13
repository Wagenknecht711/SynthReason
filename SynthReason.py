# SynthReason v7.0 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
from collections import defaultdict
import math
size = 250
memoryLimiter = 100000
import numpy as np
class Graph:
    def __init__(self, vocab_size):
        self.transition_matrix = np.zeros((vocab_size, vocab_size))
        self.start_vector = np.zeros(vocab_size)
        self.total_starts = 0
        self.word_to_index = {}
        self.index_to_word = {}
    def add_edge(self, u, v):
        if u not in self.word_to_index:
            self.word_to_index[u] = len(self.word_to_index)
            self.index_to_word[len(self.word_to_index) - 1] = u
        if v not in self.word_to_index:
            self.word_to_index[v] = len(self.word_to_index)
            self.index_to_word[len(self.word_to_index) - 1] = v
        u_index = self.word_to_index[u]
        v_index = self.word_to_index[v]
        self.transition_matrix[u_index][v_index] += 1
    def calculate_probabilities(self):
        self.transition_matrix /= np.sum(self.transition_matrix, axis=1, keepdims=True)
        self.start_vector /= self.total_starts
    def add_start(self, start):
        if start not in self.word_to_index:
            self.word_to_index[start] = len(self.word_to_index)
            self.index_to_word[len(self.word_to_index) - 1] = start
        start_index = self.word_to_index[start]
        self.start_vector[start_index] += 1
        self.total_starts += 1
    def generate_text(self, start_word, text_length):
        if start_word not in self.word_to_index:
            return "Word not found."
        current_index = self.word_to_index[start_word]
        generated_text = [start_word]
        for _ in range(1, text_length):
            next_indices = np.nonzero(self.transition_matrix[current_index])[0]
            if len(next_indices) == 0:
                break
            probs = self.transition_matrix[current_index][next_indices]
            next_index = np.random.choice(next_indices, p=probs)
            next_word = self.index_to_word[next_index]
            generated_text.append(next_word)
            current_index = next_index

        return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    filtered_words = [word for sentence in sentences for word in sentence.split() if set(sentence.split()).intersection(user_words_set)]
    return filtered_words
def create_word_graph(text):
    words = text.split()
    word_graph = Graph(len(words))
    for i in range(len(words) - 8):
        start = words[i]
        next_word = words[i + 1]
        word_graph.add_edge(start, next_word)
        word_graph.add_start(start)
    word_graph.calculate_probabilities()
    return word_graph
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
filename = "Compendium#" + str(random.randint(0, 10000000)) + ".txt"
random.shuffle(questions)
while True:
    random.shuffle(files)
    for file in files:
        with open(file, encoding="UTF-8") as f:
            text = f.read()
        user_input = input("USER: ").strip().lower()
        if not user_input:
            continue
        user_words = re.sub("\W+", " ", user_input).split()
        filtered_text = ' '.join(preprocess_text(text,user_words))[:memoryLimiter]
        word_graph = create_word_graph(filtered_text)
        generated_text = word_graph.generate_text(user_words[-1], size)
        if generated_text:
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break
