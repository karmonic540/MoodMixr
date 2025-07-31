# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause
# agents/audio_n8n_connector.py

from fastapi import FastAPI, UploadFile, File
import uvicorn
from agents.audio_agent import AudioAgent  # your existing agent logic

app = FastAPI()


@app.post("/analyze-audio/")
async def analyze_audio(file: UploadFile = File(...)):
    contents = await file.read()
    with open("temp_input.flac", "wb") as f:
        f.write(contents)

    result = AudioAgent.analyze("temp_input.flac")
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
