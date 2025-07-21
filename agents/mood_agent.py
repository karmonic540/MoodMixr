# 🎼 MoodMixr Agent: Mood Analyzer
# 🪷 Guided by Saraswati — goddess of knowledge, clarity, and sound.
# 🧠 This agent listens with purpose. Mood is not guessed — it is felt.
# © 2025 Karmonic | MoodMixr Signature Embedded
# 🎼 Agent of Saraswati — Extracts emotional truth from waveform.
from utils.constants import MOODMIXR_SIGNATURE
import librosa
import numpy as np
import cohere
import streamlit as st

co = cohere.Client(st.secrets["COHERE_API_KEY"])

class MoodClassifierAgent:
    """
    🕊️ Saraswati blesses this class — only clarity, not noise, shall pass.
    """

    @staticmethod
    def classify(track_path):
        try:
            y, sr = librosa.load(track_path)
            energy = np.mean(librosa.feature.rms(y=y))

            duration = librosa.get_duration(y=y, sr=sr)
            mood_prompt = f"This is a {round(duration)} second instrumental audio with energy level {energy:.2f}. Predict its emotional mood in 1-2 words."

            response = co.generate(
                prompt=mood_prompt,
                max_tokens=6,
                temperature=0.6
            )
            raw_mood = response.generations[0].text.strip()
            mood = MoodClassifierAgent._clean_mood(raw_mood)

            return mood, round(float(energy), 3)

        except Exception as e:
            print(f"[MoodClassifierAgent] Error: {e}")
            return "Unknown", 0.0

    @staticmethod
    def _clean_mood(mood):
        if not mood:
            return "Unknown"
        mood = mood.strip().strip(",. ")
        return mood.capitalize().replace(" ,", ",").replace("  ", " ")

# 🕉️ "This function embodies Saraswati’s clarity — only pure logic shall pass."
# 🌀 “Lord Shiva guides this transformation engine.”
