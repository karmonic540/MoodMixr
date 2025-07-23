# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 💠 MoodMixr Central Agent Router
# Modular AI agents for audio mood, energy, transitions, and external discovery

from agents.mood_agent import MoodClassifierAgent as MoodAgent
from agents.genre_classifier_agent import GenreClassifierAgent
from agents.vocal_detector_agent import VocalDetectorAgent
from agents.set_optimizer_agent import SetOptimizerAgent
from agents.summary_agent import SummaryAgent
from agents.transition_agent import TransitionRecommenderAgent
from agents.spotify_api_agent import SpotifyApiAgent


def run_moodmixr_agent(track_path):
    """
    🎧 Central MoodMixr Agent
    Runs all core audio intelligence agents on a single uploaded track.

    Parameters:
        track_path (str): Path to the uploaded audio file.

    Returns:
        dict: A structured summary containing mood, genre, vocals, bpm, key, energy,
              danceability, set role, and transition suggestions.
    """
    mood = MoodAgent.analyze(track_path)
    genre = GenreClassifierAgent.classify(track_path)
    vocals, confidence = VocalDetectorAgent.detect(track_path)
    summary = SummaryAgent.summarize(track_path)
    bpm, key = MoodAgent.detect_bpm_key(track_path)
    energy = MoodAgent.calculate_energy(track_path)
    role = SetOptimizerAgent.classify_role(bpm, energy)
    danceability = MoodAgent.calculate_danceability(track_path)
    transitions = TransitionRecommenderAgent.recommend(track_path, bpm, key, mood, energy)

    # 🎛️ Final Insight Summary Output
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
        "Danceability": danceability,
        "Suggestions": transitions
    }

def run_discover_agent(query):
    """
    🔍 Discovery Agent
    Queries Spotify for tracks matching the search string and enriches them with
    audio features like mood, energy, and BPM.

    Parameters:
        query (str): Search term (e.g., track name, artist).

    Returns:
        list: A list of enriched track dictionaries with metadata and audio insights.
    """

def run_discover_agent(query, start=0, limit=5, use_youtube_fallback=True):
    from agents.discover_agent import DiscoverAgent
    return DiscoverAgent.fetch_tracks(query, start, limit, use_youtube_fallback=use_youtube_fallback)


