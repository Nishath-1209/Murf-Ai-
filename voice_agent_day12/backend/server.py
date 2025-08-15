from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock STT + AI + TTS
@app.post("/process_audio/")
async def process_audio(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    # --- Mock: Speech-to-text ---
    transcript = "Do you remember my name?"  # Replace with real STT call

    # --- Mock: LLM Response ---
    ai_response = "Yes, I remember you said your name is Arun."

    # --- Mock: Text-to-speech output ---
    audio_output_path = os.path.join(UPLOAD_FOLDER, "response.mp3")
    with open(audio_output_path, "wb") as f:
        f.write(b"FAKEAUDIO")  # Replace with actual TTS audio bytes

    return {"transcript": transcript, "response": ai_response, "audio_url": f"/audio/response.mp3"}

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    return FileResponse(filepath, media_type="audio/mpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
