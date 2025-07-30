# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause

# moodmixr_agent.py

import os
from agents.mood_agent import MoodClassifierAgent as MoodAgent
from agents.genre_classifier_agent import GenreClassifierAgent
from agents.vocal_detector_agent import VocalDetectorAgent
from agents.set_optimizer_agent import SetOptimizerAgent
from agents.summary_agent import SummaryAgent
from agents.transition_agent import TransitionRecommenderAgent
from agents.spotify_api_agent import SpotifyApiAgent
from agents.audio_agent import AudioAnalyzerAgent
from agents.discover_agent import DiscoverAgent

def run_moodmixr_agent(track_path):
    """
    🎧 Central MoodMixr Agent
    Runs all core audio intelligence agents on a single uploaded track.

    Parameters:
        track_path (str): Path to the uploaded audio file.

    Returns:
        dict: A structured summary containing mood, genre, vocals, bpm, key, energy,
              set role, and transition suggestions.
    """
    # 🔍 Audio Features
    bpm, key = AudioAnalyzerAgent.analyze(track_path)
    mood, energy = MoodAgent.analyze(track_path)
    
    # 🧠 Additional Intelligence
    genre = GenreClassifierAgent.classify(track_path)
    vocals, confidence = VocalDetectorAgent.detect(track_path)
    role = SetOptimizerAgent.classify_role(bpm, energy)
    transitions = TransitionRecommenderAgent.recommend(
        bpm=bpm,
        key=key,
        mood=mood,
        energy=energy
    )
    summary = SummaryAgent.generate_summary(
        filename=os.path.basename(track_path),
        bpm=bpm,
        key=key,
        mood=mood,
        set_role=role,
        has_vocals=vocals
    )

    # 🎛️ Final Output (No danceability yet — can be added later via ML agent)
    return {
        "Mood": mood,
        "Genre": genre,
        "HasVocals": vocals,
        "VocalConfidence": round(confidence * 100, 1),
        "Summary": summary,
        "BPM": bpm,
        "Key": key,
        "Energy": energy,
        "SetRole": role,
        "Suggestions": transitions
    }

def run_discover_agent(query, start=0, limit=5, use_youtube_fallback=True):
    """
    🔍 Discovery Agent
    Queries Spotify (and optionally YouTube) for tracks matching the search string and
    enriches them with AI-generated audio features.

    Parameters:
        query (str): Search term (e.g., track name, artist)
        start (int): Pagination offset
        limit (int): Number of results to fetch
        use_youtube_fallback (bool): Whether to use YouTube if Spotify fails

    Returns:
        list: Enriched track dictionaries
    """
    return DiscoverAgent.fetch_tracks(query, start, limit, use_youtube_fallback)

