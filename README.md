# CodeAlpha_HealthcareChatbot
A Healthcare FAQ Chatbot built as part of the CodeAlpha AI/ML Internship Program.

## Features

* Ask healthcare-related questions in natural language
* Matches your question to the most relevant FAQ using NLP
* Displays match confidence score for every answer
* Keyword override system for critical medical terms (emergency, stroke, attack, etc.)
* Fallback message when no relevant answer is found
* Suggested questions for quick interaction
* Clean and intuitive chat interface

## Tech Stack

* **NLP**: Python + NLTK (tokenization, stopword removal, lemmatization)
* **Matching**: Scikit-learn (TF-IDF Vectorization + Cosine Similarity)
* **Frontend**: Streamlit

## How to Run

**1. Clone the repository**

```
git clone https://github.com/YOUR_USERNAME/CodeAlpha_HealthcareChatbot.git
cd CodeAlpha_HealthcareChatbot
```

**2. Install dependencies**

```
pip install streamlit nltk scikit-learn
```

**3. Run the app**

```
python -m streamlit run app.py
```

**4. Open in browser**

```
http://localhost:8501
```

## Project Structure

```
CodeAlpha_HealthcareChatbot/
├── app.py               # Main Streamlit app + NLP logic
├── faqs.py              # Healthcare FAQ dataset (20 Q&A pairs)
├── requirements.txt     # Python dependencies
└── README.md
```

## How It Works

1. User types a healthcare question in the chat input
2. NLTK preprocesses the text (lowercase, remove punctuation, tokenize, remove stopwords, lemmatize)
3. TF-IDF vectorizer converts the question into a numerical vector
4. Cosine similarity finds the closest matching FAQ from the dataset
5. If similarity is above the threshold, the best matching answer is displayed
6. If no good match is found, a fallback message is shown with helpline info

## Built for CodeAlpha Internship - Task 2
