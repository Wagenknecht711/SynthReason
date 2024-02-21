# SynthReason v9.0 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
import numpy as np
size = 250
memoryLimiter = 50000
def fit_hmm(text):
    words = text.split()
    unique_words = list(set(words))
    num_states = len(unique_words)
    transitions = np.zeros((num_states, num_states))
    initial_probs = np.zeros(num_states)
    emission_probs = np.zeros((num_states, num_states))
    emission_probs_index = {}  
    for i in range(len(words) - 1):
        u = unique_words.index(words[i])
        v = unique_words.index(words[i + 1])
        transitions[u][v] += 1
        emission_probs_index.setdefault(words[i], set()).add(words[i])
    for i, word in enumerate(words):
        if i == 0:
            initial_probs[unique_words.index(words[i+1])] += 1
    transitions /= transitions.sum(axis=1, keepdims=True)
    initial_probs /= initial_probs.sum()
    emission_probs /= emission_probs.sum(axis=1, keepdims=True)
    return transitions, initial_probs, emission_probs, unique_words, emission_probs_index
def generate_text_hmm(transitions, initial_probs, emission_probs, unique_words, start_word, emission_probs_index, text_length):
    if start_word not in emission_probs_index:
        return "Word not found."
    generated_text = []
    current_state = unique_words.index(start_word)
    for _ in range(1, text_length):
        next_state = np.random.choice(len(transitions[current_state]), p=transitions[current_state])
        next_word = np.random.choice(list(emission_probs_index[unique_words[current_state]]))
        generated_text.append(next_word)
        current_state = next_state
    return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    filtered_words = [word for sentence in sentences for word in sentence.split() if set(sentence.split()).intersection(user_words_set)]
    return filtered_words
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
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
        transitions, initial_probs, emission_probs, unique_words, emission_probs_index = fit_hmm(filtered_text)
        generated_text = generate_text_hmm(transitions, initial_probs, emission_probs, unique_words, user_words[-1], emission_probs_index, size)
        if len(generated_text) > len("Word not found."):
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break