# SynthReason v8.2 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
import numpy as np
size = 250
memoryLimiter = 50000
def fit_hmm(text):
    word_to_index = {}
    index_to_word = {}
    words = text.split()
    unique_words = list(set(words))
    for i, word in enumerate(unique_words):
        word_to_index[word] = i
        index_to_word[i] = word
    num_states = len(unique_words)
    transitions = np.zeros((num_states, num_states))
    initial_probs = np.zeros(num_states)
    emission_probs = np.zeros((num_states, num_states))
    for i in range(len(words) - 1):
        u = word_to_index[words[i]]
        v = word_to_index[words[i + 1]]
        transitions[u][v] += 1
    for i in range(len(words)):
        state = word_to_index[words[i]]
        emission_probs[state][state] += 1
    initial_probs[word_to_index[words[0]]] += 1
    transitions /= transitions.sum(axis=1, keepdims=True)
    initial_probs /= initial_probs.sum()
    emission_probs /= emission_probs.sum(axis=1, keepdims=True)
    return transitions, initial_probs, emission_probs, word_to_index, index_to_word
def generate_text_hmm(transitions, initial_probs, emission_probs, word_to_index, index_to_word, start_word, text_length):
    if start_word not in word_to_index:
        return "Word not found."
    generated_text = [start_word]
    current_state = word_to_index[start_word]
    for _ in range(1, text_length):
        next_state = np.random.choice(len(index_to_word), p=emission_probs[current_state])
        generated_text.append(index_to_word[next_state])
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
        filtered_text = ' '.join(preprocess_text(text, user_words))[:memoryLimiter]
        transitions, initial_probs, emission_probs, word_to_index, index_to_word = fit_hmm(filtered_text)
        generated_text = generate_text_hmm(initial_probs, emission_probs, transitions, word_to_index, index_to_word, user_words[-1], size)
        if generated_text:
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break