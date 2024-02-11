# SynthReason v3.2 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
from collections import defaultdict
size = 250
n = 3
class Graph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(int))
        self.transition_probabilities = defaultdict(lambda: defaultdict(float))
        self.start_probabilities = defaultdict(float)
        self.total_starts = 0
    def add_edge(self, ngram, next_word):
        self.graph[ngram][next_word] += 1
    def calculate_probabilities(self):
        for ngram in self.graph.keys():
            total_outgoing = sum(self.graph[ngram].values())
            for next_word in self.graph[ngram]:
                self.transition_probabilities[ngram][next_word] = self.graph[ngram][next_word] / total_outgoing
        for start in self.start_probabilities.keys():
            self.start_probabilities[start] = self.start_probabilities[start] / self.total_starts
    def add_start(self, start):
        self.start_probabilities[start] += 1
        self.total_starts += 1
    def generate_text(self, start_ngram, text_length):
        if start_ngram not in self.transition_probabilities:
            return "Start n-gram not found."
        current_ngram = start_ngram
        generated_text = list(current_ngram)
        while len(generated_text) < text_length:
            probabilities = list(self.transition_probabilities[current_ngram].items())
            if not probabilities:
                break
            next_words, probs = zip(*probabilities)
            next_word = random.choices(next_words, weights=probs, k=1)[0]
            generated_text.append(next_word)
            if len(generated_text) > len(start_ngram):
                current_ngram = tuple(generated_text[-len(start_ngram):])
        return ' '.join(generated_text)
def preprocess_text(text, user_words, n):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words.split())
    filtered_words = [word for sentence in sentences for word in sentence.split() if user_words_set.intersection(sentence.split())]
    ngrams = [tuple(filtered_words[i:i+n]) for i in range(len(filtered_words)-n+1)]
    return ngrams
def create_word_graph(ngrams, n=3):
    word_graph = Graph()
    for i in range(len(ngrams)-1):
        ngram, next_word = ngrams[i], ngrams[i+1][-1]
        word_graph.add_edge(ngram, next_word)
        word_graph.add_start(ngram)
    word_graph.calculate_probabilities()
    return word_graph
filename = "Compendium#" + str(random.randint(0, 10000000)) + ".txt"
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
random.shuffle(questions)
for question in questions:
    random.shuffle(files)
    for file in files:
        with open(file, encoding="UTF-8") as f:
            text = f.read()
        user_input = question.strip().lower()
        ngrams = preprocess_text(text, user_input, n)
        start_ngram = random.choice(ngrams[:-1])
        word_graph = create_word_graph(ngrams, n)
        generated_text = word_graph.generate_text(start_ngram, size)
        print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
        with open(filename, "a", encoding="utf8") as f:
            f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
        break