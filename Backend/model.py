# model.py

import re
from collections import Counter, defaultdict
import math
from functools import lru_cache

# --- Load and Preprocess Dataset ---
def words(text):
    return re.findall(r'\w+', text.lower())

with open("/home/user/Desktop/autocorrection-extension/Backend/big.txt") as f:
    WORD_LIST = words(f.read())
    WORDS = Counter(WORD_LIST)
    BIGRAMS = Counter(zip(WORD_LIST, WORD_LIST[1:]))

# --- Vocabulary and Probabilities ---
VOCAB = set(WORDS)
TOTAL = sum(WORDS.values())

def unigram_prob(word):
    return WORDS[word] / TOTAL

def bigram_prob(w1, w2):
    bigram_count = BIGRAMS[(w1, w2)]
    unigram_count = WORDS[w1]
    if unigram_count == 0:
        return 0.0
    return bigram_count / unigram_count

# --- Edit Distance ---
LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in LETTERS]
    inserts = [L + c + R for L, R in splits for c in LETTERS]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))

def known(words_set):
    return set(w for w in words_set if w in WORDS)

# --- Candidate Generator ---
def candidates(word):
    return (
        known([word])
        or known(edits1(word))
        or known(edits2(word))
        or [word]
    )

# --- Levenshtein Edit Distance ---
def edit_distance(s1, s2):
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insert = previous_row[j + 1] + 1
            delete = current_row[j] + 1
            substitute = previous_row[j] + (c1 != c2)
            current_row.append(min(insert, delete, substitute))
        previous_row = current_row
    return previous_row[-1]

# --- Error Model ---
def error_probability(word, candidate):
    if word == candidate:
        return 1.0
    else:
        return 1 / (1 + edit_distance(word, candidate))

# --- Word Correction ---
@lru_cache(maxsize=10000)
def correction(word, prev_word=None):
    candidates_list = candidates(word)
    if prev_word:
        scored = [(cand, bigram_prob(prev_word, cand) * error_probability(word, cand)) for cand in candidates_list]
    else:
        scored = [(cand, unigram_prob(cand) * error_probability(word, cand)) for cand in candidates_list]
    return max(scored, key=lambda x: x[1])[0]

# --- Sentence Corrector (Bigram-Aware) ---
def sentence_corrector(sentence):
    tokens = re.findall(r'\w+', sentence.lower())
    if not tokens:
        return ''
    corrected = [correction(tokens[0])]
    for i in range(1, len(tokens)):
        corrected.append(correction(tokens[i], corrected[i - 1]))
    return ' '.join(corrected)
