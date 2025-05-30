# 🧠 Local LLM Chat Playground

This is a minimal Python terminal application for experimenting with local LLMs and session-based memory using MongoDB. It streams AI responses like a typewriter and maintains chat history across sessions.

---

## 🚀 Features

- Connects to a local LLM server (e.g., LocalAI or OpenRouter)
- Persists chat history in MongoDB using session IDs
- Typewriter-style streaming response
- "clear" command to reset terminal view
- Adjustable model and endpoints via environment variables

---

## 🧰 Setup

### 1. Clone and prepare
```bash
git clone <this-repo-url>
cd local-models
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables (optional)
```bash
export url=http://localhost:1234              # LLM endpoint
export model=meta-llama-3.1-8b-instruct       # LLM model name
export mongo=mongodb://localhost:27017        # MongoDB URI
export OPENAI_API_KEY=dummy                   # OpenAI apikey
```

---

## 💬 Usage

### Start a new session
```bash
python app.py
```

### Resume a specific session
```bash
python app.py <existing-session-uuid>
```

### Example
```
You: Hello, what's up?
AI: I'm here and ready to assist! What's on your mind today?
```

---

## 🔄 Commands

- `clear` — Clears the terminal screen

---

## 🧠 Notes

- Sessions are UUID-based and persisted in MongoDB under `localai_experiments.chat_history`.
- Make sure your MongoDB instance is running locally or accessible via the URI.
- Ideal for experimenting with open-source models like LLaMA, Mistral, etc., via LocalAI or other compatible APIs.

---

## 🛠 Dependencies

See [`requirements.txt`](requirements.txt)

---

## 📚 Learning Goal

This project is meant to help understand:

- Prompt engineering
- Streaming LLM outputs
- Working with LangChain and MongoDB
- Local model inference via HTTP APIs

---

## 📄 License

MIT — for learning and experimentation only.
