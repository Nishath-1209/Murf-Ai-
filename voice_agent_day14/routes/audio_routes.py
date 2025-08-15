from fastapi import APIRouter, File, UploadFile
from services.stt_service import transcribe_audio
from schemas.audio_schema import AudioUploadResponse
from utils.logger import logger
import os

router = APIRouter()


@router.post("/upload-audio", response_model=AudioUploadResponse)
async def upload_audio(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    logger.info(f"Uploaded file: {file.filename}")
    transcription = transcribe_audio(file_path)
    return AudioUploadResponse(
        file_name=file.filename,
        file_size=os.path.getsize(file_path),
        content_type=file.content_type,
        transcription=transcription,
    )
