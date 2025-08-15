import librosa
import numpy as np


def analyze_audio(file_path):
    print(f"Analyzing audio file: {file_path}")
    audio_data, sr = librosa.load(file_path, sr=None)
    print(f"Audio data shape: {audio_data.shape}, Sample rate: {sr}")
    duration = librosa.get_duration(y=audio_data, sr=sr)
    tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)

    if not tempo:
        print("Failed to calculate BPM. Defaulting to 0.")
        tempo = 0.0

    return {
        "filename": file_path.split("/")[-1],
        "bpm": round(float(tempo)),  # ✅ Convert NumPy to float before round
        "duration_sec": round(float(duration)),  # ✅ Just to be safe
    }
