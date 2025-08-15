# 🎤 AI Voice Agent – 30 Days of Voice Agents Challenge

🚀 This project is part of the **#30DaysofVoiceAgents** challenge organized by **Murf AI**.  
It is a conversational voice bot built with **FastAPI**, **AssemblyAI (Speech-to-Text)**, and **Murf TTS (Text-to-Speech)**.

From Day 1 to Day 14, the bot evolved from a simple echo bot to a structured, maintainable AI-powered voice agent.

---

## 📌 Features Implemented (Day 1 → Day 14)

✅ **Day 1–5:** Basic FastAPI server, audio upload, echo bot  
✅ **Day 6–9:** Added STT (AssemblyAI) and TTS (Murf) integration  
✅ **Day 10–12:** LLM integration for conversational responses  
✅ **Day 13:** Combined STT, LLM, and TTS for a full conversation loop  
✅ **Day 14:** **Refactor & Clean Up** – Pydantic schemas, service separation, logging, linting, and GitHub upload

---

## 🛠 Tech Stack

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Speech-to-Text:** [AssemblyAI](https://www.assemblyai.com/)
- **Text-to-Speech:** [Murf AI](https://murf.ai/)
- **Language Model:** OpenAI / Any LLM API
- **Logging:** Python `logging` module
- **Code Quality:** `black`, `flake8`, `autoflake`
- **Deployment Ready:** Compatible with Uvicorn / Docker

---

## 📂 Project Structure

voice_agent/
│
├── main.py # FastAPI app entry point
│
├── routes/ # API routes
│ ├── init.py
│ ├── audio_routes.py # Audio upload, playback
│ ├── llm_routes.py # LLM chat endpoints
│
├── services/ # Third-party integrations
│ ├── init.py
│ ├── stt_service.py # AssemblyAI STT logic
│ ├── tts_service.py # Murf TTS logic
│
├── schemas/ # Pydantic models
│ ├── init.py
│ ├── audio_schema.py
│ ├── llm_schema.py
│
├── utils/ # Utility helpers
│ ├── logger.py # Central logging config
│
├── uploads/ # Stored audio files
│
├── requirements.txt # Python dependencies
└── README.md # Documentation

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

python -m venv venv
venv\Scripts\activate      # Windows

pip install -r requirements.txt


ASSEMBLYAI_API_KEY=your_assemblyai_api_key
MURF_API_KEY=your_murf_api_key
OPENAI_API_KEY=your_openai_api_key  # If LLM is used


5️⃣ Run the Application
uvicorn main:app --reload



📡 API Endpoints
🎙 Upload Audio

POST /upload-audio
Uploads an audio file and returns file info + transcription.

Request:

curl -X POST "http://127.0.0.1:8000/upload-audio" \
-F "file=@sample.wav"


Response:

{
  "file_name": "sample.wav",
  "file_size": 1048576,
  "content_type": "audio/wav",
  "transcription": "Hello world"
}

💬 Send Message to LLM

POST /chat
Sends a text message to the LLM and returns a reply.

Request:

{
  "message": "Hello, how are you?"
}


Response:

{
  "reply": "I'm great! How can I help you today?"
}

🧹 Code Quality

Format code:

black .


Remove unused imports:

autoflake --remove-all-unused-imports --recursive --remove-unused-variables .


Lint:

flake8 .

🚀 Future Improvements

Add real-time WebSocket streaming for STT

Add multiple voice options for TTS

Integrate with WhatsApp/Telegram bots

Deploy to cloud (AWS, Azure, or Render)

🙌 Credits

Murf AI – Text-to-Speech

AssemblyAI – Speech-to-Text

FastAPI – API framework