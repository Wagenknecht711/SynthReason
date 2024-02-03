# SynthReason v1.31 *ULTRA*
# Copyright 2024 George Wagenknecht
import random
import re
import math
token = "."
size = 250
with open("fileList.conf", encoding='ISO-8859-1') as f:
    files = f.read().splitlines()
print("SynthReason - Synthetic Dawn")
with open("questions.conf", encoding='ISO-8859-1') as f:
    questions = f.read().splitlines()
ngram_size = 3
while True:
    user = re.sub('\W+', ' ', input("USER: ").lower())
    random.shuffle(files)
    for file in files:
        with open(file, encoding='UTF-8') as f:
            text = f.read()
        sentences = text.split(token)
        sentences = [sentence for sentence in sentences if any(word in sentence for word in user.split())]
        random.shuffle(sentences)
        sine_frequency, cosine_frequency, amplitude, phase = 5.2, 0.5, 0.4, 1.1  # Adjust as needed
        ngrams = []
        for sentence in sentences:
            words = sentence.split()
            for i in range(len(words) - ngram_size + 1):
                ngram = words[i:i + ngram_size]
                if len(ngram) == len(set(ngram)) and i % 3 == 0:  # Check for no repeated words
                    ngram = " ".join(ngram)
                    ngrams.append(ngram)
        sine_values = [ngram.rfind(" ") / math.atan(4 / math.pi / sine_frequency * ngram.find(" ") + phase) for ngram in reversed(ngrams)]
        degrees_values = [amplitude / math.degrees(2 / math.pi / cosine_frequency * i + phase) for i in sine_values]
        combined_wave = [s * c for s, c in zip(sine_values, degrees_values)]
        def custom_sort(item):
            ngram, wave_value = item
            return (-wave_value, len(ngram))
        ngrams_with_wave = sorted(zip(ngrams, combined_wave), key=custom_sort, reverse=True)
        selected_ngrams = [ngram.split() for ngram, _ in ngrams_with_wave][:size]
        output_with_wave = ' '.join([' '.join(ngram) for ngram in selected_ngrams])
        print("\nusing:", file.strip(), "answering:", user, "\nAI:", output_with_wave, "\n\n")
        filename = "Compendium#" + str(random.randint(0, 10000000)) + ".txt"
        with open(filename, "a", encoding="utf8") as f:
            f.write("\nusing: " + file.strip() + " answering: " + user + "\n" + output_with_wave + "\n")
        break