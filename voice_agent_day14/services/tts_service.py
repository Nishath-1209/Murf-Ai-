import requests
import os

MURF_API_KEY = os.getenv("MURF_API_KEY")


def generate_tts(text: str) -> bytes:
    url = "https://api.murf.ai/speech/generate"
    headers = {"api-key": MURF_API_KEY, "Content-Type": "application/json"}
    payload = {"text": text, "voice": "some_voice_id"}
    res = requests.post(url, headers=headers, json=payload)
    return res.content
