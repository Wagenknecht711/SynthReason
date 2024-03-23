# SynthReason v18.3 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
import numpy as np
import math
from numpy.polynomial import Chebyshev as T
size = 250
n = 3
def sigmoid(x):
        return 1 / (1 + np.exp(-x))
def softmax(x):
        exp_scores = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
def fit(text):
    words = text.lower().split()
    unique_words = list(set(words))
    num_states = len(unique_words)
    transitions = np.zeros((num_states, num_states))
    keyword_frequencies = {keyword: words.index(keyword) for keyword in unique_words}
    spatial_frequency_range = np.array([keyword_frequencies[keyword] for keyword in unique_words])
    n = 0
    x = np.linspace(0, 2*np.pi, len(spatial_frequency_range))
    y = np.sin(x) + np.random.normal(scale=.1, size=x.shape) + spatial_frequency_range
    p = T.fit(x, y, n)
    for i in p:
        u, v = unique_words.index(words[n]), unique_words.index(words[n + 1])
        if u > 1 and v > 1:
            transitions[u][v] += sigmoid(i)
            n+=1
    transitions *= np.exp(transitions - np.max(transitions, axis=1, keepdims=True))
    row_sums = transitions.sum(axis=1, keepdims=True)
    transitions = np.where(row_sums > 0, transitions / row_sums, transitions)
    for i in range(num_states):
        if row_sums[i] == 0:
            transitions[i] = np.ones(num_states) / num_states
    return transitions, unique_words
def generate_text(transitions, unique_words,n_grams, start_word, text_length, n):
    if start_word not in unique_words:
        return "Word not found."
    generated_text = [start_word]
    current_state = unique_words.index(start_word)
    for _ in range(text_length - n):
        next_states = np.arange(len(transitions[current_state]))
        probabilities = transitions[current_state]
        next_state = np.random.choice(next_states, p=probabilities)
        next_word = n_grams[next_state]
        if len(re.sub(r'[^a-zA-Z0-9\s]', '', next_word)) >len(next_word)-2 and next_word not in generated_text:
            generated_text.append(next_word)
        current_state = next_state
    return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    return [word for sentence in sentences for word in sentence.split() if len(set(sentence.split()).intersection(user_words_set))>1]
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
random.shuffle(questions)
random_number = random.randint(0, 10000000)
filename = "Compendium#" + str(random_number) + ".txt"
while(True):
    random.shuffle(files)
    user_input = input("USER: ").strip().lower() 
    for file in files:
        with open(file, encoding="UTF-8") as f:
            text = f.read() 
        words = text.lower().split()
        n_grams = [' '.join(words[i:i + n]) for i in range(len(words) - n + 1)]
        user_words = re.sub("\W+", " ", user_input).split()
        filtered_text = ' '.join(preprocess_text(text, user_words))
        transitions, unique_words = fit(filtered_text)
        generated_text = generate_text(transitions, unique_words,n_grams, user_words[-1], size, n)
        if len(generated_text) > len("Word not found."):
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break
