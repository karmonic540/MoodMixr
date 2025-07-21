# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.audio_agent import AudioAnalyzerAgent
from agents.mood_agent import MoodClassifierAgent
from agents.transition_agent import TransitionRecommenderAgent
from agents.export_agent import ExportAgent
from agents.vocal_detector_agent import VocalDetectorAgent
from agents.set_optimizer_agent import SetOptimizerAgent
from agents.summary_agent import SummaryAgent

def run_moodmixr_agent(track_path):
    print("Analyzing:", track_path)

    # Core agents
    bpm, key = AudioAnalyzerAgent.analyze(track_path)
    mood, energy = MoodClassifierAgent.classify(track_path)
    transitions = TransitionRecommenderAgent.recommend(track_path, bpm, key, mood, energy)

    # New agents
    has_vocals, vocal_confidence = VocalDetectorAgent.detect(track_path)
    set_role = SetOptimizerAgent.classify_role(bpm, energy)
    summary = SummaryAgent.generate_summary(
        filename=os.path.basename(track_path),
        bpm=bpm,
        key=key,
        mood=mood,
        set_role=set_role,
        has_vocals=has_vocals
    )

    # Export (still basic)
    ExportAgent.export_metadata(track_path, bpm, key, mood, energy, transitions)

    return {
        "BPM": bpm,
        "Key": key,
        "Mood": mood,
        "Energy": energy,
        "Suggestions": transitions,
        "SetRole": set_role,
        "HasVocals": has_vocals,
        "VocalConfidence": vocal_confidence,
        "Summary": summary
    }
