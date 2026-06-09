# CodeAlpha_HealthcareChatbot

A Healthcare FAQ Chatbot built as part of the **CodeAlpha AI/ML Internship Program** (Task 2).

## Features

- Ask healthcare-related questions in natural language
- Covers symptoms, diseases, medications, nutrition, mental health, first aid, and more
- Typing indicator and smooth chat UI
- Quick-question buttons for common topics
- Auto disclaimer for medical responses
- Emergency guidance (112 / 911)
- **No server required** — runs entirely in the browser

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **AI Backend:** Claude API (Anthropic) — called client-side
- **Hosting:** GitHub Pages (static site)

## Live Demo

[View the live site](https://weiwei-gitch.github.io/CodeAlpha_HealthcareChatbot/)

## How to Run Locally

Simply open `index.html` in any browser — no installation needed.

```bash
git clone https://github.com/weiwei-gitch/CodeAlpha_HealthcareChatbot.git
cd CodeAlpha_HealthcareChatbot
open index.html   # or double-click the file
```

## Deployment

This project is deployed via **GitHub Pages** as a fully static site.

To deploy your own copy:

1. Fork or clone this repository
2. Go to **Settings → Pages**
3. Set the source branch to `main` and folder to `/ (root)`
4. GitHub Pages will serve `index.html` automatically

## Project Structure

```
CodeAlpha_HealthcareChatbot/
├── index.html        # Main app (HTML + CSS + JS in one file)
└── README.md
```

## How It Works

The chatbot sends user questions to the Claude API directly from the browser. A detailed healthcare-focused system prompt keeps responses medically relevant, safe, and appropriately disclaimed. No Python, no Flask, no Streamlit — just static HTML.

## Disclaimer

This chatbot provides **general health information only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for personal medical concerns.

## License

Built for educational purposes as part of the CodeAlpha AI/ML Internship Program.
