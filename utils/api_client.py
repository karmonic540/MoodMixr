# utils/api_client.py

import requests


def call_audio_agent_api(file_path):
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "audio/mpeg")}
        response = requests.post("http://localhost:8000/analyze", files=files)
        return response.json()


def call_mood_agent_api(file_path):
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f, "audio/mpeg")}
        response = requests.post("http://localhost:8001/analyze", files=files)
        return response.json()
