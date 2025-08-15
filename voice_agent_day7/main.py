from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import shutil
import requests
import time

load_dotenv()
app = FastAPI()

# Static and template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
MURF_API_URL = "https://api.murf.ai/v1/speech/generate"

class TTSRequest(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Text-to-Speech via Murf
@app.post("/generate")
def generate_audio(req: TTSRequest):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY
    }
    payload = {
        "text": req.text,
        "voice_id": "en-US-cooper"
    }
    response = requests.post(MURF_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to generate audio")
    data = response.json()
    return {"audio_url": data.get("audioFile")}

# Echo Bot V2: Transcribe + TTS
@app.post("/tts/echo")
async def tts_echo(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Upload to AssemblyAI
        headers = {"authorization": ASSEMBLYAI_API_KEY}
        with open(file_path, "rb") as f:
            upload_res = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, data=f)
        upload_url = upload_res.json()["upload_url"]

        # Request transcription
        transcript_res = requests.post(
            "https://api.assemblyai.com/v2/transcript",
            json={"audio_url": upload_url},
            headers=headers
        )
        transcript_id = transcript_res.json()["id"]

        # Poll until done
        while True:
            poll_res = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcript_id}", headers=headers).json()
            if poll_res["status"] == "completed":
                transcription = poll_res["text"]
                break
            elif poll_res["status"] == "error":
                raise HTTPException(status_code=500, detail="Transcription failed")
            time.sleep(1)

        # Send transcription to Murf
        murf_headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "api-key": MURF_API_KEY
        }
        murf_payload = {
            "text": transcription,
            "voice_id": "en-US-cooper"
        }
        murf_res = requests.post(MURF_API_URL, headers=murf_headers, json=murf_payload)
        if murf_res.status_code != 200:
            raise HTTPException(status_code=500, detail="Murf TTS failed")
        murf_data = murf_res.json()
        return {"audio_url": murf_data.get("audioFile")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))