# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence

import tempfile
import requests
import numpy as np
import librosa
import os

from utils.utils import search_spotify_track, get_spotify_audio_features
from agents.youtube_fallback_agent import YouTubeFallbackAgent


class DiscoverAgent:
    @staticmethod
    def fetch_tracks(query, start=0, limit=5, use_youtube_fallback=True):
        enriched = []
        results = search_spotify_track(query)
        sliced_results = results[start : start + limit]

        for track in sliced_results:
            bpm = 0
            key = "Unknown"
            energy = 0.0
            danceability = 0.0
            mood = "Chill"
            use_fallback = False
            file_path = None

            # Try Spotify audio features first
            features = get_spotify_audio_features(track["id"])
            if features and features.get("tempo"):
                try:
                    bpm = round(features.get("tempo", 0))
                    key = features.get("key", "Unknown")
                    energy = round(features.get("energy", 0.0), 2)
                    danceability = round(features.get("danceability", 0.0), 2)
                    mood = (
                        "Energetic"
                        if energy > 0.6
                        else "Chill"
                        if energy < 0.3
                        else "Groovy"
                    )
                except Exception as e:
                    print(f"[Spotify Audio Feature Error] {e}")
                    use_fallback = True
            else:
                use_fallback = True

            # 🔁 Fallback logic (only if allowed)
            if use_youtube_fallback and use_fallback:
                if not track.get("preview_url"):
                    print(f"[MoodMixr] Falling back to YouTube for: {track['name']}")
                    file_path, yt_url = YouTubeFallbackAgent.download_audio(query)
                else:
                    print(
                        f"[MoodMixr] Using Spotify preview for Librosa fallback: {track['name']}"
                    )
                    try:
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".mp3"
                        ) as tmp:
                            audio_data = requests.get(track["preview_url"]).content
                            tmp.write(audio_data)
                            file_path = tmp.name
                    except Exception as e:
                        print(f"[Fallback] Failed to fetch preview: {e}")
                        file_path = None

                # 📊 Analyze fallback audio with Librosa
                if file_path:
                    try:
                        y, sr = librosa.load(file_path, sr=None)
                        if len(y) < sr * 10:  # less than 10 seconds
                            raise ValueError("Audio clip too short for analysis")

                        bpm = round(librosa.beat.tempo(y, sr=sr)[0])
                        energy = float(np.mean(librosa.feature.rms(y=y)))
                        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
                        key_index = np.argmax(np.mean(chroma, axis=1))
                        key = [
                            "C",
                            "C#",
                            "D",
                            "D#",
                            "E",
                            "F",
                            "F#",
                            "G",
                            "G#",
                            "A",
                            "A#",
                            "B",
                        ][key_index]
                        mood = (
                            "Energetic"
                            if energy > 0.6
                            else "Chill"
                            if energy < 0.3
                            else "Groovy"
                        )
                    except Exception as e:
                        print(f"[Librosa Error] for {track['name']}: {e}")

            print(
                f"🎯 Final: {track['name']} → BPM: {bpm}, Energy: {energy}, Mood: {mood}, Key: {key}"
            )
            enriched.append(
                {
                    "name": track["name"],
                    "artist": track["artist"],
                    "album": track["album"],
                    "image": track["image"],
                    "preview_url": track.get("preview_url"),
                    "id": track["id"],
                    "bpm": bpm,
                    "key": key,
                    "energy": energy,
                    "danceability": danceability,
                    "mood": mood,
                    "source": "Spotify Features"
                    if not use_fallback
                    else "Fallback Analysis",
                    "youtube_url": yt_url,
                }
            )

        return enriched
