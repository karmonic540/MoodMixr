# ⛩️ MoodMixr Utility Core
# 🎛️ Built by Karmonic for sacred creative intelligence and modular clarity
# 🧠 Purpose: Handle audio processing, mood detection, waveform rendering, transition logic, and platform sync
# Created: 2025-07-21 | License: MIT + Karma Clause

# === IMPORTS ===
import os, json, base64, io, hashlib, requests
import numpy as np
import pandas as pd
import librosa, librosa.display
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
import cohere
from mutagen import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from PIL import Image

# === SECRET MANAGEMENT ===
def get_secret(key):
    return st.secrets.get(key) or os.getenv(key)

# === AUDIO PROCESSING ===
def load_audio(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)
        return y, sr
    except Exception as e:
        print(f"[Utils] Audio load error: {e}")
        return None, None

def detect_bpm_key(y, sr):
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][np.argmax(np.mean(chroma, axis=1)) % 12]
    return int(tempo), key

def calculate_energy_profile(y):
    return float(np.mean(librosa.feature.rms(y=y)[0])) * 1000

# === MOOD + COLOR ===
def analyze_mood(audio_path):
    try:
        co = cohere.Client(get_secret("COHERE_API_KEY"))
        prompt = f"Analyze the mood of this audio track based on its name: {os.path.basename(audio_path)}"
        response = co.generate(model='command-light', prompt=prompt, max_tokens=20)
        return response.generations[0].text.strip()
    except Exception:
        return "Unknown / Neutral"

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

# === DJ ROLE + TRANSITIONS ===
def classify_set_role(bpm, energy, mood):
    mood = mood.lower()
    if bpm < 90 or "chill" in mood:
        return "🎬 Opener"
    elif energy > 60 and bpm >= 120:
        return "🔥 Peak"
    elif 90 <= bpm < 120 and energy < 60:
        return "🎧 Mid-Set"
    elif energy < 40:
        return "🎉 Closer"
    return "🎚️ Support"

def suggest_best_transitions(track_data):
    def score(a, b):
        s = 100 - abs(a['bpm'] - b['bpm'])
        if a['key'] == b['key']: s += 15
        if a['mood'].split()[0].lower() in b['mood'].lower(): s += 10
        return s

    results = []
    for i, track in enumerate(track_data):
        best = max(
            (b for j, b in enumerate(track_data) if i != j),
            key=lambda b: score(track, b)
        )
        reason = f"Close BPM ({track['bpm']}→{best['bpm']}), "
        reason += "Key match ✅, " if track['key'] == best['key'] else ""
        reason += "Similar mood 🎭" if track['mood'].split()[0].lower() in best['mood'].lower() else "Mood contrast"
        results.append({"from": track['filename'], "to": best['filename'], "score": score(track, best), "reason": reason})
    return results

# === WAVEFORM + ENERGY FLOW VISUALS ===
def generate_plotly_energy_curve(tracks):
    import plotly.graph_objects as go

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

    # Glow effect and polished theme
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

# === ALBUM ART ===
from mutagen import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from PIL import Image
import io

def extract_album_art(audio_path):
    """
    Extract embedded album art from audio metadata (FLAC/MP3).

    Args:
        audio_path (str): Full path to audio file.

    Returns:
        PIL.Image or None: Album art image or None if not found.
    """
    try:
        metadata = MutagenFile(audio_path)
        if metadata is None:
            return None

        if isinstance(metadata, FLAC):
            pics = metadata.pictures
            if pics:
                return Image.open(io.BytesIO(pics[0].data))
        elif isinstance(metadata, MP3):
            for tag in metadata.tags.values():
                if tag.FrameID == "APIC":
                    return Image.open(io.BytesIO(tag.data))
        return None
    except Exception as e:
        print(f"[AlbumArt] Error: {e}")
        return None



# === YOUTUBE INTEGRATION ===
def search_youtube_videos(query, max_results=5, api_key=None):
    if not api_key:
        raise ValueError("YouTube API key is required.")
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
    if not api_key:
        raise ValueError("YouTube API key is required.")
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
    except Exception as e:
        return None

def analyze_youtube_track(video_url, title="Track"):
    from pytube import YouTube
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        if not stream:
            raise ValueError("No downloadable stream found.")
        path = stream.download(output_path="app/audio", filename=f"{title.replace(' ', '_')}_temp.mp3")

        y, sr = librosa.load(path, sr=None)
        bpm, key = detect_bpm_key(y, sr)
        mood = analyze_mood(path)
        energy = calculate_energy_profile(y)
        fig = generate_emotion_waveform(y, sr, mood, title)

        return {"bpm": bpm, "key": key, "energy": energy, "mood": mood, "fig": fig}
    except Exception as e:
        return {"error": str(e)}
# === ALBUM ART & TRACK METADATA ===

def extract_album_art(audio_path):
    """
    Extract embedded album art from audio metadata (FLAC/MP3).
    """
    try:
        metadata = MutagenFile(audio_path)
        if metadata is None:
            return None

        if isinstance(metadata, FLAC):
            pics = metadata.pictures
            if pics:
                return Image.open(io.BytesIO(pics[0].data))
        elif isinstance(metadata, MP3):
            for tag in metadata.tags.values():
                if tag.FrameID == "APIC":
                    return Image.open(io.BytesIO(tag.data))
        return None
    except Exception as e:
        print(f"[AlbumArt] Error: {e}")
        return None

def extract_track_metadata(audio_path):
    """
    Extract track metadata: artist, title, album (from FLAC/MP3 headers).
    """
    try:
        meta = {}
        file = MutagenFile(audio_path, easy=True)

        if isinstance(file, FLAC):
            meta["artist"] = file.get("artist", ["Unknown"])[0]
            meta["title"] = file.get("title", ["Unknown"])[0]
            meta["album"] = file.get("album", ["Unknown"])[0]
        elif isinstance(file, MP3):
            meta["artist"] = file.get("artist", ["Unknown"])[0]
            meta["title"] = file.get("title", ["Unknown"])[0]
            meta["album"] = file.get("album", ["Unknown"])[0]

        return meta
    except Exception as e:
        print(f"[Metadata] Error: {e}")
        return {"artist": "Unknown", "title": "Unknown", "album": "Unknown"}