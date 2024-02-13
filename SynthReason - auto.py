# SynthReason v6.3 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
from collections import defaultdict

size = 250

class Graph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(int))
        self.transition_probabilities = defaultdict(lambda: defaultdict(float))
        self.start_probabilities = defaultdict(float)
        self.total_starts = 0

    def add_edge(self, u, v):
        self.graph[u][v] += 1

    def calculate_probabilities(self):
        for u in self.graph.keys():
            total_outgoing = sum(self.graph[u].values())
            for v in self.graph[u]:
                self.transition_probabilities[u][v] = self.graph[u][v] / total_outgoing
                for start in self.start_probabilities.keys():
                    self.start_probabilities[start] /= self.transition_probabilities[u][v]
    def add_start(self, start):
        self.start_probabilities[start] += 1
        self.total_starts += 1

    def generate_text(self, start_word, text, text_length):
        if start_word not in self.transition_probabilities:
            return "Word not found."  
    
        current_word = start_word
        generated_text = [current_word]
    
        while len(generated_text) < text_length:
            if current_word not in self.transition_probabilities:
                # If current word has no associated probabilities, add default probabilities
                next_words = list(self.graph[current_word].keys())
                default_prob = 1 / len(next_words)
            else:
                # Use existing probabilities
                probabilities = list(self.transition_probabilities[current_word].items())
                if not probabilities:
                    break
                next_words, probs = zip(*probabilities)
                # Calculate default probability based on the number of next words
                default_prob = 1 / len(next_words)
            
            # Update probabilities based on the current word
            for i in text[:size]:
                updated_probs = [self.transition_probabilities[next_word].get(i, default_prob) for next_word in next_words]
            
            next_word = random.choices(next_words, weights=updated_probs, k=1)[0]
            generated_text.append(next_word)
            current_word = next_word
    
        return ' '.join(generated_text)


def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    filtered_words = [word for sentence in sentences for word in sentence.split() if set(sentence.split()).intersection(user_words_set)]
    return filtered_words

def create_word_graph(text):
    words = text.split()
    word_graph = Graph()
    for i in range(len(words)-5):
        start, next_word = words[i+4], words[i + 5]
        word_graph.add_edge(start, next_word)
        if i == 0 or words[i-1] in '.!?':
            word_graph.add_start(start)
    word_graph.calculate_probabilities()
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
        filtered_text = ' '.join(preprocess_text(text,user_words))
        word_graph = create_word_graph(filtered_text)
        generated_text = word_graph.generate_text(user_words[-1],filtered_text.split(), size)
        if generated_text:
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break
