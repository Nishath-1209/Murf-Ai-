import requests
import os

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def transcribe_audio(file_path: str) -> str:
    headers = {"authorization": ASSEMBLYAI_API_KEY}
    with open(file_path, "rb") as f:
        upload_res = requests.post(
            "https://api.assemblyai.com/v2/upload", headers=headers, data=f
        )
    upload_url = upload_res.json()["upload_url"]

    transcribe_res = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=headers,
        json={"audio_url": upload_url},
    )
    return transcribe_res.json()
