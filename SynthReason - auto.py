# SynthReason v14.4 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
import numpy as np
import math
size = 250
n = 3
num_choices = 3
memoryLimiter = 50000
cognitionThreshold = 10000
magic = 20
sine_frequency = 50.2
amplitude = 100.4
phase = 71.1
def fit(text):
    words = text.lower().split()
    unique_words = list(set(words))
    num_states = len(unique_words)
    transitions = np.zeros((num_states, num_states))
    keyword_frequencies = {keyword: words.index(keyword) for keyword in unique_words}
    spatial_frequency_range = np.array([keyword_frequencies[keyword] for keyword in unique_words])
    n = 0
    for i in spatial_frequency_range:
        u, v = unique_words.index(words[n]), unique_words.index(words[n + 1])
        if u > 1 and v > 1:
            transitions[u][v] += n
            n+=1
    transitions *= np.array([amplitude * (magic/ math.pi / sine_frequency * math.acosh(i + phase)) for i in spatial_frequency_range])
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
    for _ in range(text_length - n):
        next_states = np.arange(len(transitions[current_state]))
        probabilities = transitions[current_state]
        next_state = np.random.choice(next_states, p=probabilities)
        next_word = unique_words[next_state]
        if len(re.sub(r'[^a-zA-Z0-9\s]', '', next_word)) >len(next_word)-2:
            generated_text.append(next_word)
        current_state = next_state
        if current_state ==  next_state+4:
            current_state = len(unique_words) - 1
        elif current_state ==  _ - 1:
            next_state+4
    return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    return [word for sentence in sentences for word in sentence.split() if set(sentence.split()).intersection(user_words_set)]
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
random.shuffle(questions)
random_number = random.randint(0, 10000000)
filename = "Compendium#" + str(random_number) + ".txt"
for question in questions:
    random.shuffle(files)
    user_input = question.strip().lower() 
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