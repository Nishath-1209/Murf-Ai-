from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path
import shutil
import os
import requests

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Environment and API Key
MURF_API_KEY = os.getenv("MURF_API_KEY")
MURF_API_URL = "https://api.murf.ai/v1/speech/generate"

# Define Uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount static and templates folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ------------------ TTS Endpoint ------------------

class TTSRequest(BaseModel):
    text: str

@app.post("/generate-audio")
def generate_audio(request: TTSRequest):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY
    }
    payload = {
        "text": request.text,
        "voice_id": "en-US-cooper"
    }
    response = requests.post(MURF_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    data = response.json()
    return {"audio_url": data.get("audioFile")}

# ------------------ Voices List ------------------

@app.get("/voices")
def get_voices():
    url = "https://api.murf.ai/v1/speech/voices"
    headers = {
        "api-key": MURF_API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()

# ------------------ Upload Audio Endpoint (Day 5) ------------------

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_location)

    return JSONResponse({
        "filename": file.filename,
        "content_type": file.content_type,
        "size_in_bytes": file_size
    })

# ------------------ Root Route ------------------

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
