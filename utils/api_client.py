# utils/api_client.py

import requests


def call_mood_agent_api(file_path: str):
    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "audio/wav")}
            response = requests.post("http://localhost:8000/analyze", files=files)

        return response.json()
    except Exception as e:
        return {"error": str(e)}


def call_audio_agent_api(file_path: str):
    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "audio/wav")}
            response = requests.post("http://localhost:8001/analyze", files=files)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
