# 🎧 MoodMixr Agent: Mood Analyzer
# 🕉️ Guided by Saraswati – goddess of clarity, sound, and wisdom.
# 🔍 Extracts emotional truth from waveform using AI and energy patterns.

from utils.constants import MOODMIXR_SIGNATURE
import librosa
import numpy as np
import cohere
import streamlit as st

co = cohere.Client(st.secrets["COHERE_API_KEY"])

class MoodClassifierAgent:
    """
    Saraswati blesses this class — only clarity, not noise, shall pass.
    """

    @staticmethod
    def analyze(track_path):
        """
        Analyzes audio to classify mood using waveform and energy.

        Parameters:
            track_path (str): Path to the uploaded audio file.

        Returns:
            tuple: (mood_label, energy_score)
        """
        try:
            y, sr = librosa.load(track_path)
            energy = np.mean(librosa.feature.rms(y=y))

            duration = librosa.get_duration(y=y, sr=sr)
            mood_prompt = (
                f"This is a {round(duration)} second instrumental audio with "
                f"energy level {energy:.2f}. Predict the overall mood."
            )

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
        mood = mood.strip().strip(".")
        return mood.capitalize().replace(" .", ".").replace(" .", " ")

# 🟣 "This function embodies Saraswati’s clarity – only pure logic shall pass."
# 🔱 "Lord Shiva guides this transformation engine."
