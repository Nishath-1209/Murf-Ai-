from pydantic import BaseModel
from typing import Optional


class AudioUploadResponse(BaseModel):
    file_name: str
    file_size: int
    content_type: str
    transcription: Optional[str] = None
