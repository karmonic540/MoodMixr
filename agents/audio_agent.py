# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause

# agents/audio_agent.py

import sys
import json
import librosa


def analyze_audio(path):
    try:
        y, sr = librosa.load(path)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo_val = float(tempo[0]) if hasattr(tempo, "__getitem__") else float(tempo)

        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        key_index = chroma.mean(axis=1).argmax()

        key_map = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        musical_key = key_map[key_index % 12]

        duration = librosa.get_duration(y=y, sr=sr)

        result = {
            "bpm": round(tempo_val),
            "key": musical_key,
            "duration_sec": round(duration, 2),
            "track_path": path,
        }

        print(json.dumps(result))  # ✅ Critical: Return JSON to n8n

    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    track_path = sys.argv[1]
    analyze_audio(track_path)

# 🌐 A fusion of AI + Human creativity, built with sacred precision.
