# main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import assemblyai as aai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

aai.settings.api_key = API_KEY

app = FastAPI()

# CORS setup if frontend is connected
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe/file")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save file temporarily
    with open(file.filename, "wb") as f:
        f.write(await file.read())

    # Transcribe using AssemblyAI SDK
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file.filename)

    # Delete temporary file
    os.remove(file.filename)

    return {"transcript": transcript.text}
