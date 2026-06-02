import html
import streamlit as st
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from faqs import faqs
 
# ── Download required NLTK data ──────────────────────────────────────────────
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
 
# ── NLP helpers ───────────────────────────────────────────────────────────────
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
 
# Keyword → FAQ index mapping for critical medical terms that TF-IDF may miss
KEYWORD_OVERRIDES = {
    "emergency": 4, "emergencies": 4, "urgent": 4, "critical": 4,
    "attack": 4, "heart attack": 4, "silent attack": 4, "stroke": 4,
    "unconscious": 4, "faint": 4, "collapse": 4, "accident": 4,
    "ambulance": 15, "ambulances": 15,
    "icu": 17, "intensive care": 17, "critical care": 17,
    "teleconsult": 5, "online consult": 5, "video consult": 5,
    "report": 6, "lab report": 6, "test result": 6, "blood test": 6,
    "second opinion": 16,
    "medical record": 18, "records": 18,
    "parking": 19,
    "pharmacy": 8, "medicine": 8, "drug": 8,
    "pediatric": 14, "children": 14, "child": 14, "nicu": 14, "newborn": 14,
    "cancel": 9, "reschedule": 9,
    "payment": 10, "pay": 10, "upi": 10, "cash": 10,
    "canteen": 11, "cafeteria": 11, "food": 11,
    "certificate": 12, "medical certificate": 12,
    "covid": 13, "corona": 13, "mask": 13,
}
 
 
def preprocess(text: str) -> str:
    """Lowercase → remove punctuation → tokenize → remove stopwords → lemmatize."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t not in stop_words]
    return " ".join(tokens)
 
 
# ── Build TF-IDF index once (cached) ─────────────────────────────────────────
@st.cache_resource
def build_index():
    questions = [faq["question"] for faq in faqs]
    processed = [preprocess(q) for q in questions]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(processed)
    return vectorizer, matrix
 
 
vectorizer, tfidf_matrix = build_index()
 
THRESHOLD = 0.10
 
 
def get_best_answer(user_input: str):
    """Return (answer, score) for the best-matching FAQ."""
    lower_input = user_input.lower()
 
    # 1. Check keyword overrides first (handles "silent attack" → emergency etc.)
    for keyword, idx in KEYWORD_OVERRIDES.items():
        if keyword in lower_input:
            return faqs[idx]["answer"], 1.0
 
    # 2. Fall back to TF-IDF cosine similarity
    processed_input = preprocess(user_input)
    input_vec = vectorizer.transform([processed_input])
    scores = cosine_similarity(input_vec, tfidf_matrix).flatten()
    best_idx = scores.argmax()
    best_score = scores[best_idx]
    if best_score < THRESHOLD:
        return None, best_score
    return faqs[best_idx]["answer"], best_score
 
 
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediAssist · Healthcare FAQ Bot",
    page_icon="🏥",
    layout="centered",
)
 
# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');
 
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #f0f4f8;
    }
 
    /* ── Header banner ── */
    .header-banner {
        background: linear-gradient(135deg, #0d3b66 0%, #1a6e9f 60%, #57b8e0 100%);
        border-radius: 18px;
        padding: 2rem 2.5rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(13,59,102,0.25);
        position: relative;
        overflow: hidden;
    }
    .header-banner::after {
        content: "🏥";
        position: absolute;
        right: 2rem; top: 50%;
        transform: translateY(-50%);
        font-size: 4rem;
        opacity: 0.18;
    }
    .header-banner h1 {
        font-family: 'DM Serif Display', serif;
        color: #ffffff;
        font-size: 2rem;
        margin: 0 0 0.3rem;
    }
    .header-banner p {
        color: #cce8f5;
        font-size: 0.92rem;
        margin: 0;
        font-weight: 300;
    }
 
    /* ── Chat bubbles ── */
    .bubble-wrap { display: flex; margin-bottom: 1rem; align-items: flex-end; gap: 0.6rem; }
    .bubble-wrap.user  { flex-direction: row-reverse; }
    .bubble-wrap.bot   { flex-direction: row; }
 
    .avatar {
        width: 36px; height: 36px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem; flex-shrink: 0;
    }
    .avatar.user { background: #0d3b66; color: #fff; }
    .avatar.bot  { background: #e0f2fe; color: #0d3b66; }
 
    .bubble {
        max-width: 76%;
        padding: 0.75rem 1.1rem;
        border-radius: 18px;
        font-size: 0.93rem;
        line-height: 1.55;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    .bubble.user {
        background: #0d3b66;
        color: #ffffff !important;
        border-bottom-right-radius: 4px;
    }
    .bubble.bot {
        background: #ffffff;
        color: #1e293b !important;
        border-bottom-left-radius: 4px;
        border: 1px solid #e2eaf2;
    }
    .bubble.bot.fallback {
        background: #fff8e1;
        border-color: #ffe082;
        color: #5d4037 !important;
    }
 
    /* ── Score badge ── */
    .score-badge {
        font-size: 0.7rem;
        color: #94a3b8;
        margin-top: 0.3rem;
        padding-left: 0.4rem;
    }
 
    /* ── Suggested questions ── */
    .suggestions-title {
        font-size: 0.78rem;
        color: #64748b;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 1.2rem 0 0.5rem;
        font-weight: 500;
    }
 
    /* ── Input area — force visible dark text ── */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 1.5px solid #bcd4e6 !important;
        padding: 0.65rem 1rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.92rem !important;
        background: #ffffff !important;
        color: #1e293b !important;
        caret-color: #0d3b66 !important;
        -webkit-text-fill-color: #1e293b !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input::placeholder {
        color: #94a3b8 !important;
        -webkit-text-fill-color: #94a3b8 !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1a6e9f !important;
        box-shadow: 0 0 0 3px rgba(26,110,159,0.12) !important;
        color: #1e293b !important;
        -webkit-text-fill-color: #1e293b !important;
    }
 
    /* ── Buttons ── */
    .stButton > button {
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        border: 1.5px solid #bcd4e6 !important;
        background: #ffffff !important;
        color: #0d3b66 !important;
        padding: 0.35rem 0.85rem !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover {
        background: #e0f2fe !important;
        border-color: #1a6e9f !important;
    }
 
    /* ── Divider ── */
    hr { border-color: #dde7f0 !important; }
 
    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)
 
# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="header-banner">
        <h1>MediAssist</h1>
        <p>Your 24 × 7 Healthcare FAQ Assistant &nbsp;·&nbsp; Ask anything about appointments, services &amp; more</p>
    </div>
    """,
    unsafe_allow_html=True,
)
 
# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "text": "👋 Hello! I'm MediAssist, your healthcare FAQ bot. Ask me about appointments, visiting hours, lab reports, insurance, emergency services, and more.",
            "score": None,
            "fallback": False,
        }
    ]
 
# ── Render chat history ───────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = "👤" if role == "user" else "🏥"
        fallback_cls = "fallback" if msg.get("fallback") else ""
        # Escape HTML in message text to prevent tags like </div> breaking layout
        safe_text = html.escape(msg["text"])
 
        st.markdown(
            f"""
            <div class="bubble-wrap {role}">
                <div class="avatar {role}">{avatar}</div>
                <div>
                    <div class="bubble {role} {fallback_cls}">{safe_text}</div>
                    {"" if msg.get("score") is None else
                     f'<div class="score-badge">Match confidence: {msg["score"]:.0%}</div>'}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
 
st.markdown("---")
 
# ── Suggested questions ───────────────────────────────────────────────────────
SUGGESTIONS = [
    "How do I book an appointment?",
    "What are visiting hours?",
    "Is there a 24/7 pharmacy?",
    "How do I get my lab reports?",
    "Do you accept insurance?",
    "What to do in an emergency?",
]
 
st.markdown('<p class="suggestions-title">💡 Suggested Questions</p>', unsafe_allow_html=True)
cols = st.columns(3)
for i, suggestion in enumerate(SUGGESTIONS):
    if cols[i % 3].button(suggestion, key=f"sug_{i}"):
        answer, score = get_best_answer(suggestion)
        st.session_state.messages.append({"role": "user", "text": suggestion, "score": None, "fallback": False})
        if answer:
            st.session_state.messages.append({"role": "bot", "text": answer, "score": score, "fallback": False})
        else:
            st.session_state.messages.append({
                "role": "bot",
                "text": "⚠️ I'm sorry, I couldn't find a relevant answer. Please call our helpline or visit the reception for assistance.",
                "score": score,
                "fallback": True,
            })
        st.rerun()
 
# ── User input ────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    user_input = col1.text_input(
        "Type your question…",
        placeholder="e.g. How do I cancel my appointment?",
        label_visibility="collapsed",
    )
    submitted = col2.form_submit_button("Send ➤")
 
if submitted and user_input.strip():
    answer, score = get_best_answer(user_input.strip())
    st.session_state.messages.append({"role": "user", "text": user_input.strip(), "score": None, "fallback": False})
    if answer:
        st.session_state.messages.append({"role": "bot", "text": answer, "score": score, "fallback": False})
    else:
        st.session_state.messages.append({
            "role": "bot",
            "text": "⚠️ I'm sorry, I couldn't find a relevant answer to your question. Please contact our helpline for further assistance.",
            "score": score,
            "fallback": True,
        })
    st.rerun()
 
# ── Clear chat button ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)