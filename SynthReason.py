# SynthReason v20.2 *MASTER*
# Copyright 2024 George Wagenknecht
import re
import random
import numpy as np
def fit(text):
    words = text.lower().split()
    num_states = len(words)
    transitions = np.zeros((num_states, num_states))
    for i in range(len(words) - 1):
        current_word = words[i]
        next_word = words[i + 1]
        current_index = words.index(current_word)
        next_index = words.index(next_word)
        transitions[current_index][next_index] += 1
    row_sums = np.sum(transitions, axis=1, keepdims=True)
    if np.any(row_sums == 0):
        print("Warning: Zero row sums detected in transition matrix. Setting probabilities for those states to uniform distribution.")
        zero_row_indices = np.where(row_sums == 0)[0]
        transitions[zero_row_indices, :] = 1 / len(transitions)  # Set zero probabilities to uniform distribution
    transitions /= row_sums
    return transitions, words
def generate_text(transitions, words, start_word, text_length):
    generated_text = [start_word]
    current_word = start_word
    for _ in range(text_length - 1):
        current_index = words.index(current_word)
        next_index = np.random.choice(range(len(transitions[current_index])), p=transitions[current_index])
        next_word = words[next_index]
        generated_text.append(next_word)
        current_word = next_word
    generated_text = [re.sub(r'[^a-zA-Z]', '', word) for word in generated_text]
    return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = re.split(r'(?<=[.!?])\s+', text.lower())
    user_words_set = set(user_words)
    return [word for sentence in sentences for word in sentence.split() if len(set(sentence.split()).intersection(user_words_set)) > 1]
with open("FileList.conf", encoding="ISO-8859-1") as f:
    files = f.read().splitlines()
with open("questions.conf", encoding="ISO-8859-1") as f:
    questions = f.read().splitlines()
random.shuffle(files)
random_number = random.randint(0, 10000000)
filename = "Compendium#" + str(random_number) + ".txt"
while True:
    user_input = input("USER: ").strip().lower()
    for file in files:
        with open(file, encoding="UTF-8") as f:
            text = f.read() 
        user_words = re.sub("\W+", " ", user_input).split()
        filtered_text = ' '.join(preprocess_text(text, user_words))
        transitions, words = fit(filtered_text)
        if user_words[-1] in words:
            generated_text = generate_text(transitions, words, user_words[-1], 250)
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break
