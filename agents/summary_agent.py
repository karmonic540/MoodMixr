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

class SummaryAgent:
    """
    🎶 Krishna smiles through this summary — may it charm every set with elegance.
    """

    @staticmethod
    def generate_summary(filename, bpm, key, mood, set_role, has_vocals):
        mood_clean = mood.title()
        vocal_text = "Vocals" if has_vocals else "No Vocals"
        return f"{filename} | {bpm} BPM | {key} | {mood_clean} | {set_role} | {vocal_text}"

    
# 🕉️ "This function embodies Saraswati’s clarity — only pure logic shall pass."
# 🌀 “Lord Shiva guides this transformation engine.”
