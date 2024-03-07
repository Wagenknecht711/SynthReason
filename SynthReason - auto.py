# SynthReason v14.7 *ULTRA*
# Copyright 2024 George Wagenknecht
import random
import math
size = 100
n = 3
precision = 1
memoryLimiter = 50000
def fit(text):
    words = text.lower().split()
    unique_words = list(set(words))
    num_states = len(unique_words)
    transitions = [[0] * num_states for _ in range(num_states)]
    keyword_frequencies = {keyword: words.index(keyword) for keyword in unique_words}
    for i in range(len(words) - 1):
        u, v = unique_words.index(words[i]), unique_words.index(words[i + 1])
        if u > 1 and v > 1:
            transitions[u][v] += i
    for j in range(num_states):
        spatial_frequency_range = [keyword_frequencies[unique_words[j]] for _ in range(num_states)]
        for i, u in enumerate(spatial_frequency_range):
            transitions[j][i] *= u
    for i in range(num_states):
        row_sum = sum(transitions[i])
        if row_sum == 0:
            transitions[i] = [1 / num_states] * num_states
        else:
            transitions[i] = [transitions[i][j] / row_sum for j in range(num_states)]
    return transitions, unique_words
def generate_text(transitions, unique_words, start_word, text_length, n):
    if start_word not in unique_words:
        return "Word not found."
    generated_text = [start_word]
    current_state = unique_words.index(start_word)
    for _ in range(text_length - n):
        next_states = list(range(len(transitions[current_state])))
        probabilities = transitions[current_state]
        next_state = random.choices(next_states, weights=probabilities)[0]
        next_word = unique_words[next_state]
        if len(''.join(filter(str.isalnum, next_word))) > len(next_word) - 2:
            generated_text.append(next_word)
        current_state = next_state
    return ' '.join(generated_text)
def preprocess_text(text, user_words):
    sentences = text.lower().split('. ')
    user_words_set = set(user_words)
    filtered_words = []
    for sentence in sentences:
        for word in sentence.split():
            if len(set(sentence.split()).intersection(user_words_set)) > precision:
                filtered_words.append(word)
    return filtered_words[:memoryLimiter]
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
        transitions, unique_words = fit(filtered_text)
        generated_text = sorted(generate_text(transitions, unique_words, user_words[-1], size, n).split("."))[0] + "."
        if len(generated_text) > len("Word not found."):
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break