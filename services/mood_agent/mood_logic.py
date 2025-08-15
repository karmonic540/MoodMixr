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

        print(f"Analyzing mood and energy for file: {file_path}")
        print(f"Audio data shape: {audio_data.shape}, Sample rate: {sr}")

        if not tempo:
            print("Failed to calculate BPM. Defaulting to 0.")
            tempo = 0.0

        if not rms:
            print("Failed to calculate RMS energy. Defaulting to 0.")
            rms = 0.0

        mood = "Energetic" if tempo > 120 and rms > 0.04 else "Calm"
        energy = round(rms * 100, 2)

        return {
            "filename": file_path.split("/")[-1],
            "bpm": round(tempo),
            "energy": round(energy, 2),
            "mood": mood,
        }

    except (ValueError, FileNotFoundError) as e:
        print(f"🔥 Librosa failed: {str(e)}")
        return {"error": f"Librosa failed: {str(e)}"}
