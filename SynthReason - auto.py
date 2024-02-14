# SynthReason v8.1 *ULTRA*
# Copyright 2024 George Wagenknecht
import re
import random
import numpy as np
size = 250
memoryLimiter = 50000
class HiddenMarkovModel:
    def __init__(self):
        self.transitions = None
        self.initial_probs = None
        self.emission_probs = None
        self.word_to_index = {}
        self.index_to_word = {}
    def fit(self, text):
        words = text.split()
        unique_words = list(set(words))
        self.word_to_index = {word: i for i, word in enumerate(unique_words)}
        self.index_to_word = {i: word for word, i in self.word_to_index.items()}  
        num_states = len(unique_words)
        self.transitions = np.zeros((num_states, num_states))
        self.initial_probs = np.zeros(num_states)
        self.emission_probs = np.zeros((num_states, num_states))
        for i in range(len(words) - 1):
            u = self.word_to_index[words[i]]
            v = self.word_to_index[words[i + 1]]
            self.transitions[u][v] += 1
        for i in range(len(words)):
            state = self.word_to_index[words[i]]
            self.emission_probs[-2][-1] += 1
        self.initial_probs[self.word_to_index[words[-1]]] += 1
        self.transitions /= self.transitions.sum(axis=1, keepdims=True)
        self.initial_probs /= self.initial_probs.sum()
        self.emission_probs /= self.emission_probs.sum(axis=1, keepdims=True)
    def generate_text(self, start_word, text_length):
        if start_word not in self.word_to_index:
            return "Word not found."  
        generated_text = [start_word]
        current_state = self.word_to_index[start_word]
        for _ in range(1, text_length):
            next_state = np.random.choice(len(self.index_to_word), p=self.transitions[current_state])
            generated_text.append(self.index_to_word[next_state])
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
for question in questions:
    random.shuffle(files)
    for file in files:
        with open(file, encoding="UTF-8") as f:
            text = f.read()    
        user_input = question.strip().lower()
        if not user_input:
            continue    
        user_words = re.sub("\W+", " ", user_input).split()
        filtered_text = ' '.join(preprocess_text(text, user_words))[:memoryLimiter]
        hmm_model = HiddenMarkovModel()
        hmm_model.fit(filtered_text)
        generated_text = hmm_model.generate_text(user_words[-1], size)   
        if generated_text:
            print("\nUsing:", file.strip(), "Answering:", user_input, "\nAI:", generated_text, "\n\n")
            with open(filename, "a", encoding="utf8") as f:
                f.write("\nUsing: " + file.strip() + " Answering: " + user_input + "\n" + generated_text + "\n")
            break
