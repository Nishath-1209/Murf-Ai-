    # 🎙️ AI Voice Agent - 30 Days of AI Voice Agents Challenge

This project is part of the **#30DaysofVoiceAgents** challenge by **Murf AI**, where I built an AI-powered voice bot step-by-step over 30 days.  
The bot can listen to your voice, understand what you said, and reply back — in a natural Murf voice!

---

## 🚀 Features
- **🎤 Real-time Voice Recording** — Capture voice input directly from the browser.
- **🧠 AI-powered Understanding** — Transcribes speech using **AssemblyAI**.
- **🗣️ Murf TTS Integration** — Converts AI responses to human-like speech.
- **🔁 Echo Bot Mode** — Repeats back what you said in Murf's voice.
- **🤖 LLM Mode** — Responds intelligently using an LLM API.
- **🌐 FastAPI Backend** — Handles audio uploads, transcription, and TTS generation.

---

## 🛠 Technologies Used
- **Frontend** — HTML, JavaScript, Fetch API
- **Backend** — Python, FastAPI
- **Speech-to-Text (STT)** — [AssemblyAI]
- **Text-to-Speech (TTS)** — [Murf AI]
- **AI Model** — Any LLM endpoint (configurable)
- **Others** — `uvicorn` for running the server

---

## 🏗 Architecture

🎤 User Voice
↓
Browser (Recorder) → Backend (FastAPI) → AssemblyAI (STT)
↓ ↓
Murf AI (TTS) ← AI Response ← LLM ← Backend
↓
🔊 Audio Output