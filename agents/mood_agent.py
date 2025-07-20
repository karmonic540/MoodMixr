import librosa
import numpy as np
import cohere
import streamlit as st

co = cohere.Client(st.secrets["COHERE_API_KEY"])

class MoodClassifierAgent:

    @staticmethod
    def classify(track_path):
        try:
            y, sr = librosa.load(track_path)
            energy = np.mean(librosa.feature.rms(y=y))

            # AI Mood prompt
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
