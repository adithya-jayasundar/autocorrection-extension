# 🧠 Autocorrection System with Chrome Extension

This project was built as part of my **Natural Language Processing (NLP) course project**. It implements a **probabilistic autocorrect system from scratch** and deploys it as a live Chrome Extension using **ngrok** to serve the backend locally. The model runs efficiently without any machine learning training — relying purely on language statistics and string similarity techniques.

---

## 📌 Project Highlights

- ✍️ Built an autocorrector using:
  - **Unigram Language Model** to score word probabilities
  - **Noisy Channel Model** for candidate generation and correction using edit operations (insert, delete, substitute, transpose)
- 🧪 Trained on a **6.6M word dataset** from:
  - Project Gutenberg (public domain books)
  - British National Corpus (BNC)
  - Vocabulary.com word lists
- 🔁 Handles:
  - **Non-word errors** (e.g., “lanuage” → “language”)
  - **Real-word errors** (context-independent)
- 🚀 **Deployed as a Chrome Extension**
  - Uses **ngrok** to tunnel local backend
  - Provides real-time autocorrection in any input field on websites

---



