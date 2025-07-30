# ⛩️ MoodMixr Utility Core
# 🎛️ Built by Karmonic for sacred creative intelligence and modular clarity
# 🧠 Purpose: Handle audio processing, mood detection, waveform rendering, transition logic, and platform sync
# Created: 2025-07-21 | License: MIT + Karma Clause

import os, json, requests, io
import numpy as np
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from mutagen import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from PIL import Image

from agents.spotify_api_agent import SpotifyApiAgent

# === SECRETS ===
def get_secret(key):
    return st.secrets.get(key) or os.getenv(key)

# === FILE + AUDIO HANDLING ===
def load_audio(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)
        return y, sr
    except Exception as e:
        print(f"[Utils] Audio load error: {e}")
        return None, None

# === ALBUM ART + METADATA ===
def extract_album_art(audio_path):
    try:
        metadata = MutagenFile(audio_path)
        if metadata is None: return None
        if isinstance(metadata, FLAC) and metadata.pictures:
            return Image.open(io.BytesIO(metadata.pictures[0].data))
        elif isinstance(metadata, MP3):
            for tag in metadata.tags.values():
                if tag.FrameID == "APIC":
                    return Image.open(io.BytesIO(tag.data))
        return None
    except Exception as e:
        print(f"[AlbumArt] Error: {e}")
        return None

def extract_track_metadata(audio_path):
    try:
        meta = {}
        file = MutagenFile(audio_path, easy=True)
        meta["artist"] = file.get("artist", ["Unknown"])[0]
        meta["title"] = file.get("title", ["Unknown"])[0]
        meta["album"] = file.get("album", ["Unknown"])[0]
        return meta
    except Exception as e:
        print(f"[Metadata] Error: {e}")
        return {"artist": "Unknown", "title": "Unknown", "album": "Unknown"}

# === MOOD COLOR + UI SUPPORT ===
def get_mood_color(mood):
    mood = mood.lower()
    return {
        "happy": "#FF9900",
        "calm": "#00CCFF",
        "dark": "#9900FF",
        "energetic": "#FF0033",
        "romantic": "#FF9A9E",
        "sad": "#9E9E9E"
    }.get(mood.split()[0], "#00FF99")

def get_bpm_animation_speed(bpm):
    return "1.2s" if bpm < 80 else "1s" if bpm < 100 else "0.8s" if bpm < 120 else "0.6s"

# === WAVEFORM VISUALIZATION (Optional: move to agent later) ===
def generate_plotly_energy_curve(tracks):
    energies = [t["energy"] for t in tracks]
    labels = [t["filename"] for t in tracks]
    moods = [t["mood"] for t in tracks]
    colors = [get_mood_color(mood) for mood in moods]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(labels))),
        y=energies,
        mode='lines+markers+text',
        text=labels,
        textposition="top center",
        line=dict(color="white", width=2, shape='spline'),
        marker=dict(size=14, color=colors, line=dict(color="#222", width=1)),
        hoverinfo='text+y'
    ))

    fig.update_layout(
        title="🔋 DJ Set Energy Flow",
        template="plotly_dark",
        height=420,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(title="Energy", showgrid=True),
        plot_bgcolor="#0D0D0D",
        paper_bgcolor="#0D0D0D",
        font=dict(family="Poppins, sans-serif", color="white")
    )
    return fig

# === SPOTIFY ===
def get_spotify_client():
    return SpotifyApiAgent()

def search_spotify_track(query):
    spotify = get_spotify_client()
    results = spotify.search(query)
    tracks = results.get("tracks", {}).get("items", [])
    return [{
        "id": t["id"],
        "name": t["name"],
        "artist": t["artists"][0]["name"],
        "album": t["album"]["name"],
        "preview_url": t["preview_url"],
        "image": t["album"]["images"][0]["url"] if t["album"]["images"] else ""
    } for t in tracks]

def get_spotify_audio_features(track_id):
    spotify = get_spotify_client()
    return spotify.get_audio_features(track_id)

# === YOUTUBE ===
def search_youtube_videos(query, max_results=5, api_key=None):
    if not api_key: raise ValueError("YouTube API key is required.")
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet", "q": query, "type": "video",
        "videoEmbeddable": "true", "maxResults": max_results, "key": api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return [{
            "videoId": i["id"]["videoId"],
            "title": i["snippet"]["title"],
            "channel": i["snippet"]["channelTitle"],
            "thumbnail": i["snippet"]["thumbnails"]["high"]["url"]
        } for i in response.json().get("items", [])]
    except requests.exceptions.RequestException as e:
        st.error(f"YouTube API Error: {e}")
        return []

def get_youtube_video_details(video_id, api_key=None):
    if not api_key: raise ValueError("YouTube API key is required.")
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        item = response.json()["items"][0]
        return {
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "published": item["snippet"]["publishedAt"],
            "duration": item["contentDetails"]["duration"]
        }
    except Exception:
        return None
