# SynthReason v16.5 *EPIC*
# Copyright 2024 George Wagenknecht
import random
import math
size = 50
n = 3
n2 = 16
precision = 2
def fit(text, n):
    words = text.lower().split()
    unique_words = list(set(words))
    num_states = len(unique_words)
    ngrams = [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]
    transitions = [[0] * num_states for _ in range(num_states)]
    for i in range(len(transitions) - 1):
        keyword_frequencies = {keyword: ngrams.count(keyword) for keyword in set(ngrams)}
        spatial_frequency_range = [keyword_frequencies[ngrams[j]] for j in range(len(ngrams))]
        u, v = unique_words.index(words[i-1]), unique_words.index(words[i])
        if u > 1 and v > 1:
            transitions[u][v] += 1
        for j, u in enumerate(spatial_frequency_range):
            transitions[-1][i] *= 1
    for i in range(num_states):
        row_sum = sum(transitions[i])
        if row_sum == 0:
            transitions[i] = [1 / num_states] * num_states
        else:
            transitions[i] = [transitions[i][j] / row_sum for j in range(num_states)]
    return transitions, unique_words, ngrams
def generate_text(transitions, unique_words, ngrams, start_ngram, text_length, n):
    if start_ngram not in unique_words:
        return "N-gram not found."
    generated_text = start_ngram.split()
    current_state = unique_words.index(start_ngram)
    for _ in range(text_length - n):
        next_states = list(range(len(transitions[current_state])))
        probabilities = transitions[current_state]
        next_state = random.choices(next_states, weights=probabilities)[0]
        if next_state < len(ngrams):
            next_ngram = ngrams[next_state]
            next_word = next_ngram.split()[-1]
        if len(''.join(filter(str.isalnum, next_word))) > len(next_word) - 2 and next_word not in generated_text:
            generated_text.append(next_ngram)
        current_state = next_state
    return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = text.lower().split('.')
    user_words_set = set(user_words)
    filtered_words = []
    for sentence in sentences:
        if len(set(sentence.split()).intersection(user_words_set)) > precision:
            filtered_words.append(sentence)
    return filtered_words
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
        user_words = ''.join(e if e.isalnum() or e.isspace() else ' ' for e in user_input).split()
        filtered_text = ' '.join(preprocess_text(text, user_words))
        transitions, unique_words, ngrams = fit(filtered_text,n2)
        generated_text = generate_text(transitions, unique_words, ngrams, user_words[-1], size, n)
        if len(generated_text) > len("Word not found."):
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break
