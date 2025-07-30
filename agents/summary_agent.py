# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause
# 🎭 MoodMixr Agent: Track Summary
# 🎻 Guided by Krishna — storyteller of vibe, charm, and rhythm.
# 📝 This agent turns data into mood poetry.
# © 2025 Karmonic | MoodMixr Signature Embedded
# 🎭 Agent of Krishna — Turns data into emotion, stats into story.

from utils.constants import MOODMIXR_SIGNATURE

import cohere
import streamlit as st

co = cohere.Client(st.secrets["COHERE_API_KEY"])

class SummaryAgent:
    """
    Krishna smiles through this summary — may it charm every set with elegance.
    This agent turns track metadata into a poetic set summary.
    """

    @staticmethod
    def generate_summary(filename, bpm, key, mood, set_role, has_vocals):
        prompt = (
            f"Create a 1-line summary for a DJ track with the following metadata:\n"
            f"Filename: {filename}\n"
            f"BPM: {bpm}\n"
            f"Key: {key}\n"
            f"Mood: {mood}\n"
            f"Set Role: {set_role}\n"
            f"Vocals: {'Yes' if has_vocals else 'No'}\n\n"
            f"Summary:"
        )

        try:
            response = co.generate(
                prompt=prompt,
                max_tokens=60,
                temperature=0.7
            )
            summary = response.generations[0].text.strip()
            return summary

        except Exception as e:
            print(f"[SummaryAgent] Cohere error: {e}")
            # graceful fallback
            return f"{filename} | BPM: {bpm} | Key: {key} | Mood: {mood} | Role: {set_role} | Vocals: {'Yes' if has_vocals else 'No'}"


    
# 🕉️ "This function embodies Saraswati’s clarity — only pure logic shall pass."
# 🌀 “Lord Shiva guides this transformation engine.”
