import librosa
import numpy as np


def analyze_audio(file_path):
    audio_data, sr = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=audio_data, sr=sr)
    tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)

    return {
        "filename": file_path.split("/")[-1],
        "bpm": round(float(tempo)),  # ✅ Convert NumPy to float before round
        "duration_sec": round(float(duration)),  # ✅ Just to be safe
    }
