# 🎧 MoodMixr Agent: Mood Analyzer
# 🕉️ Guided by Saraswati – goddess of clarity, sound, and wisdom.
# 🔍 Extracts emotional truth from waveform using AI and energy patterns.

# 🎧 MoodMixr Agent: Mood Analyzer
# 🕉️ Guided by Saraswati – goddess of clarity, sound, and wisdom.
# 🔍 Extracts emotional truth from waveform using AI and spectral patterns.

# 🎧 MoodMixr Agent: Mood Analyzer v2
# 🕉️ Guided by Saraswati – reads waveform truth, not words.

import librosa
import numpy as np
import streamlit as st
from utils.constants import MOODMIXR_SIGNATURE

class MoodClassifierAgent:
    VALID_MOODS = [
        "Energetic", "Aggressive", "Uplifting", "Romantic",
        "Chill", "Melancholy", "Dark", "Calm"
    ]

@staticmethod
def analyze(track_path):
    try:
        y, sr = librosa.load(track_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        tempo = librosa.beat.tempo(y=y, sr=sr)[0]
        rms = librosa.feature.rms(y=y).flatten()
        energy = float(np.mean(rms))
        spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        percussive = librosa.effects.percussive(y)
        harmonic = librosa.effects.harmonic(y)
        perc_energy = float(np.mean(librosa.feature.rms(y=percussive).flatten()))
        harm_energy = float(np.mean(librosa.feature.rms(y=harmonic).flatten()))
        perc_ratio = perc_energy / (harm_energy + 1e-6)

        # === SCORE VECTORS ===
        mood_profiles = {
            "Energetic":     {"tempo": 130, "energy": 0.06, "perc_ratio": 1.1, "spectral_centroid": 3500},
            "Aggressive":    {"tempo": 128, "energy": 0.08, "perc_ratio": 1.4, "spectral_centroid": 4000},
            "Uplifting":     {"tempo": 120, "energy": 0.05, "perc_ratio": 0.9, "spectral_centroid": 3000},
            "Romantic":      {"tempo": 110, "energy": 0.045, "perc_ratio": 0.7, "spectral_centroid": 2500},
            "Chill":         {"tempo": 105, "energy": 0.03, "perc_ratio": 0.5, "spectral_centroid": 2000},
            "Melancholy":    {"tempo": 90,  "energy": 0.02, "perc_ratio": 0.3, "spectral_centroid": 1800},
            "Calm":          {"tempo": 80,  "energy": 0.015,"perc_ratio": 0.2, "spectral_centroid": 1600},
            "Dark":          {"tempo": 60,  "energy": 0.01, "perc_ratio": 0.1, "spectral_centroid": 1200}
        }

        def similarity_score(mood, profile):
            return (
                -abs(tempo - profile["tempo"]) * 0.25 +
                -abs(energy - profile["energy"]) * 150 +
                -abs(perc_ratio - profile["perc_ratio"]) * 10 +
                -abs(spectral_centroid - profile["spectral_centroid"]) * 0.01
            )

        best_mood = "Unknown"
        best_score = -float("inf")
        for mood, profile in mood_profiles.items():
            score = similarity_score(mood, profile)
            if score > best_score:
                best_score = score
                best_mood = mood

        return best_mood, round(energy, 3)

    except Exception as e:
        print(f"[MoodClassifierAgent] Error: {e}")
        return "Unknown", 0.0




# 🔱 May Saraswati guide this analysis to purity. No ego, no noise — just emotion and pattern.
