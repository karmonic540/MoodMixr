# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 🧠 MoodMixr Central Agent Router
# Modular AI agents for audio mood, energy, transitions, and external discovery

from agents.mood_agent import MoodAgent
from agents.genre_classifier_agent import GenreClassifierAgent
from agents.vocal_detector_agent import VocalDetectorAgent
from agents.set_optimizer_agent import SetOptimizerAgent
from agents.summary_agent import SummaryAgent
from agents.transition_agent import TransitionRecommenderAgent

def run_moodmixr_agent(track_path):
    mood = MoodAgent.analyze(track_path)
    genre = GenreClassifierAgent.classify(track_path)
    vocals, confidence = VocalDetectorAgent.detect(track_path)
    summary = SummaryAgent.summarize(track_path)
    bpm, key = MoodAgent.detect_bpm_key(track_path)
    energy = MoodAgent.calculate_energy(track_path)
    role = SetOptimizerAgent.classify_role(bpm, energy)
    transitions = TransitionRecommenderAgent.recommend(track_path, bpm, key, mood, energy)

    return {
        "Mood": mood,
        "Genre": genre,
        "HasVocals": vocals,
        "VocalConfidence": confidence,
        "Summary": summary,
        "BPM": bpm,
        "Key": key,
        "Energy": energy,
        "SetRole": role,
        "Suggestions": transitions
    }

def run_discover_agent(query):
    from agents.discover_agent import DiscoverAgent  # 👈 local import to avoid circular error
    return DiscoverAgent.fetch_tracks(query)
