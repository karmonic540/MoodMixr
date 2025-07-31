# services/mood_agent/mood_logic.py

import librosa
import numpy as np


def analyze_mood_energy(file_path):
    try:
        print(f"🧠 Analyzing file: {file_path}")
        audio_data, sr = librosa.load(file_path, sr=None)
        print(f"🎧 Loaded audio: {audio_data.shape}, Sample Rate: {sr}")
        rms = float(np.mean(librosa.feature.rms(y=audio_data)))  # ✅ Cast to float
        tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
        tempo = float(tempo)  # ✅ Cast to float

        mood = "Energetic" if tempo > 120 and rms > 0.04 else "Calm"
        energy = round(rms * 100, 2)

        return {
            "filename": file_path.split("/")[-1],
            "bpm": round(tempo),
            "energy": round(energy, 2),
            "mood": mood,
        }

    except Exception as e:
        print(f"🔥 Librosa failed: {str(e)}")
        return {"error": f"Librosa failed: {str(e)}"}
