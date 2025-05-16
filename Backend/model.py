# model.py

import re
from collections import Counter
import math

# --- Load and Preprocess Dataset ---
def words(text):
    return re.findall(r'\w+', text.lower())

with open("/home/user/Desktop/autocorrection-extension/Backend/big.txt") as f:
    WORDS = Counter(words(f.read()))

# --- Vocabulary and Probability ---
VOCAB = set(WORDS)
TOTAL = sum(WORDS.values())

def P(word):
    """Probability of a word"""
    return WORDS[word] / TOTAL

# --- Edit Distance 1 ---
LETTERS = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in LETTERS]
    inserts = [L + c + R for L, R in splits for c in LETTERS]
    return set(deletes + transposes + replaces + inserts)

# --- Known words from edits ---
def known(words):
    return set(w for w in words if w in WORDS)

# --- Candidate Corrections ---
def candidates(word):
    return (
        known([word])
        or known(edits1(word))
        or [word]
    )

# --- Error Model ---
def error_probability(word, candidate):
    """
    Error model: assume fixed cost for edit.
    You can refine this using confusion matrices or frequencies.
    """
    if word == candidate:
        return 1.0
    else:
        return 1 / (1 + edit_distance(word, candidate))  # lower distance = higher prob

# --- Edit Distance (Levenshtein Distance) ---
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

# --- Noisy Channel Correction ---
def correction(word):
    candidates_list = candidates(word)
    scored = [(cand, P(cand) * error_probability(word, cand)) for cand in candidates_list]
    return max(scored, key=lambda x: x[1])[0]

# --- Sentence Corrector ---
def sentence_corrector(sentence):
    tokens = re.findall(r'\w+', sentence.lower())
    corrected = [correction(token) for token in tokens]
    return ' '.join(corrected)
