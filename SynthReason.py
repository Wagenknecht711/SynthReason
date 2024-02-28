# SynthReason v10.4 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
import numpy as np
import math
size = 250
n = 2
num_choices = 3
memoryLimiter = 50000
cognitionThreshold = 10000
sine_frequency = 50.2
amplitude = 10.4
phase = 11.1
def fit(text):
    words = text.lower().split()
    unique_words = list(set(words))
    num_states = len(unique_words)
    transitions = np.zeros((num_states, num_states))
    for i in range(len(words) - 1):
        u, v = unique_words.index(words[i]), unique_words.index(words[i + 1])
        if u > 1 and v > 1:
            transitions[u][v] += cognitionThreshold
    keyword_frequencies = {keyword: words.index(keyword) for keyword in unique_words}
    spatial_frequency_range = np.array([keyword_frequencies[keyword] for keyword in unique_words])
    transitions *= np.array([amplitude * math.atan(2/ math.pi / sine_frequency * i + phase) for i in spatial_frequency_range])
    row_sums = transitions.sum(axis=1, keepdims=True)
    transitions = np.where(row_sums != 0, transitions / row_sums, transitions)
    for i in range(num_states):
        if row_sums[i] == 0:
            transitions[i] = np.ones(num_states) / num_states
    return transitions, unique_words
def generate_text(transitions, unique_words, start_word, text_length, n, num_choices):
    if start_word not in unique_words:
        return "Word not found."
    generated_text = [start_word]
    current_state = unique_words.index(start_word)
    snake_direction = 1
    for _ in range(text_length - n):
        next_states = np.arange(len(transitions[current_state]))
        probabilities = transitions[current_state]   
        if snake_direction == 1:
            next_state = np.random.choice(next_states, p=probabilities)
        else:
            next_state = np.random.choice(next_states[::-1], p=probabilities[::-1])
        next_word = unique_words[next_state]
        generated_text.append(next_word)
        if next_state == len(unique_words) - 1 or next_state == 0:
            snake_direction *= -1
        current_state = next_state
    return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    return [word for sentence in sentences for word in sentence.split() if set(sentence.split()).intersection(user_words_set)]
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
random_number = random.randint(0, 10000000)
filename = "Compendium#" + str(random_number) + ".txt"
while True:
    random.shuffle(files)
    user_input = input("USER: ").strip().lower() 
    for file in files:
        with open(file, encoding="UTF-8") as f:
            text = f.read() 
        user_words = re.sub("\W+", " ", user_input).split()
        filtered_text = ' '.join(preprocess_text(text, user_words))[:memoryLimiter]
        transitions, unique_words = fit(filtered_text)
        generated_text = generate_text(transitions, unique_words, user_words[-1], size, n, num_choices)
        if len(generated_text) > len("Word not found."):
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break