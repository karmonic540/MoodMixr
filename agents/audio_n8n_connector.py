# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause
# agents/audio_n8n_connector.py

import sys
import json
import requests
import librosa


def analyze_audio(path):
    y, sr = librosa.load(path)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # 🛠️ Fix: ensure tempo is a scalar (not array)
    if hasattr(tempo, "item"):
        tempo = tempo.item()

    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    key_index = chroma.mean(axis=1).argmax()
    key_map = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    key = key_map[key_index % 12]
    duration = librosa.get_duration(y=y, sr=sr)

    return {
        "bpm": round(tempo),
        "key": key,
        "duration_sec": round(duration, 2),
        "track_path": path,
    }


if __name__ == "__main__":
    audio_path = sys.argv[1]

    try:
        result = analyze_audio(audio_path)

        # 🔁 Update this if you're using production mode
        webhook_url = "http://localhost:5678/webhook-test/analyze-audio"

        response = requests.post(webhook_url, json=result)

        print("✅ Sent to n8n")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

    except Exception as e:
        print("❌ Error:", str(e))
