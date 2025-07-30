# === utils.py (Refactored and Documented) ===

# Grouped imports for clarity
import os
import json
import base64
import requests
import librosa
import librosa.display
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
import cohere


# Unified secret access
def get_secret(key):
    """
    Fetch a secret value from Streamlit secrets or environment variables.

    Args:
        key (str): The key for the secret.

    Returns:
        str: The secret value, or None if not found.
    """
    return st.secrets.get(key) or os.getenv(key)


# BPM and Key Detection
def detect_bpm_key(y, sr):
    """
    Detect the BPM and key of an audio signal.

    Args:
        y (np.ndarray): Audio time series.
        sr (int): Sampling rate of the audio.

    Returns:
        tuple: BPM (int) and key (str).
    """
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    key = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][
        np.argmax(np.mean(chroma, axis=1)) % 12
    ]
    return int(tempo), key


# Mood Analysis via Cohere
def analyze_mood(audio_path):
    """
    Analyze the mood of an audio track using Cohere's AI model.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        str: The detected mood.
    """
    try:
        co = cohere.Client(get_secret("COHERE_API_KEY"))
        prompt = f"Analyze the mood of this audio track based on its name: {os.path.basename(audio_path)}"
        response = co.generate(model="command-light", prompt=prompt, max_tokens=20)
        return response.generations[0].text.strip()
    except Exception:
        return "Unknown / Neutral"


# Energy Calculation
def calculate_energy_profile(y):
    """
    Calculate the energy profile of an audio signal.

    Args:
        y (np.ndarray): Audio time series.

    Returns:
        float: Energy value.
    """
    return float(np.mean(librosa.feature.rms(y=y)[0])) * 1000


# Mood Color Map
def get_mood_color(mood):
    """
    Map a mood to a corresponding color.

    Args:
        mood (str): Mood description.

    Returns:
        str: Hex color code.
    """
    mood = mood.lower()
    return {
        "happy": "#FF9900",
        "uplifting": "#FF9900",
        "calm": "#00CCFF",
        "chill": "#00CCFF",
        "dark": "#9900FF",
        "emotional": "#9900FF",
        "energetic": "#FF0033",
        "hype": "#FF0033",
    }.get(mood.split()[0], "#00FF99")


# BPM to Animation Speed
def get_bpm_animation_speed(bpm):
    """
    Determine the animation speed based on BPM.

    Args:
        bpm (int): Beats per minute.

    Returns:
        str: CSS animation speed.
    """
    return (
        "1.2s" if bpm < 80 else "1s" if bpm < 100 else "0.8s" if bpm < 120 else "0.6s"
    )


# Classify DJ Set Role
def classify_set_role(bpm, energy, mood):
    """
    Classify the DJ set role based on BPM, energy, and mood.

    Args:
        bpm (int): Beats per minute.
        energy (float): Energy level.
        mood (str): Mood description.

    Returns:
        str: DJ set role emoji.
    """
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


# Suggest DJ Transitions
def suggest_best_transitions(track_data):
    """
    Suggest the best transitions between tracks for a DJ set.

    Args:
        track_data (list): List of track information dictionaries.

    Returns:
        list: List of suggested transitions with details.
    """

    def score(a, b):
        s = 100 - abs(a["bpm"] - b["bpm"])
        if a["key"] == b["key"]:
            s += 15
        if a["mood"].split()[0].lower() in b["mood"].lower():
            s += 10
        return s

    results = []
    for i, track in enumerate(track_data):
        best = max(
            (b for j, b in enumerate(track_data) if i != j),
            key=lambda b: score(track, b),
        )
        reason = f"Close BPM ({track['bpm']}→{best['bpm']}), "
        reason += "Key match ✅, " if track["key"] == best["key"] else ""
        reason += (
            "Similar mood 🎭"
            if track["mood"].split()[0].lower() in best["mood"].lower()
            else "Mood contrast"
        )
        results.append(
            {
                "from": track["filename"],
                "to": best["filename"],
                "score": score(track, best),
                "reason": reason,
            }
        )
    return results


# Plotly Energy Curve
def generate_plotly_energy_curve(tracks):
    """
    Generate a Plotly line curve chart for track energy levels.

    Args:
        tracks (list): List of track information dictionaries.

    Returns:
        plotly.graph_objs.Figure: Plotly figure object.
    """
    energies = [t["energy"] for t in tracks]
    labels = [t["filename"] for t in tracks]
    moods = [t["mood"] for t in tracks]
    colors = [get_mood_color(mood) for mood in moods]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=list(range(len(labels))),
            y=energies,
            mode="lines+markers",
            marker=dict(size=12, color=colors),
            line=dict(color="white"),
            text=labels,
            hoverinfo="text+y",
        )
    )
    for i, label in enumerate(labels):
        fig.add_annotation(
            x=i,
            y=energies[i] + 5,
            text=label[:20] + "...",
            showarrow=False,
            font=dict(color=colors[i], size=12),
        )
    fig.update_layout(
        title="🎚️ DJ Set Energy Flow",
        template="plotly_dark",
        height=400,
        xaxis=dict(showticklabels=False),
        yaxis_title="Energy",
    )
    return fig


# Waveform Generation
def generate_emotion_waveform(y, sr, mood="neutral", track_name=""):
    """
    Generate an emotion-based waveform plot for an audio track.

    Args:
        y (np.ndarray): Audio time series.
        sr (int): Sampling rate of the audio.
        mood (str): Mood description.
        track_name (str): Name of the track.

    Returns:
        matplotlib.figure.Figure: Matplotlib figure object.
    """
    mood_color_map = {
        "happy": "gold",
        "calm": "skyblue",
        "dark": "purple",
        "energetic": "crimson",
        "neutral": "#00FF99",
    }
    mood_key = next((k for k in mood_color_map if k in mood.lower()), "neutral")
    color = mood_color_map[mood_key]

    fig, ax = plt.subplots(figsize=(10, 3), facecolor="#0D0D0D")
    ax.set_facecolor("#0D0D0D")
    librosa.display.waveshow(y, sr=sr, ax=ax, color=color, alpha=0.9)
    ax.set_title(
        "🎧 Audio Waveform (Emotion-Based)", color="white", fontsize=12, loc="left"
    )
    ax.text(
        1.0,
        1.0,
        f"🎵 {track_name}",
        ha="right",
        va="top",
        transform=ax.transAxes,
        fontsize=10,
        color="#AAAAAA",
    )
    ax.text(
        0,
        1.0,
        f"🎨 Emotion Color: {color}",
        ha="left",
        va="top",
        transform=ax.transAxes,
        fontsize=9,
        color=color,
    )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout()
    return fig


# YouTube Search
def search_youtube_videos(query, max_results=5, api_key=None):
    """
    Search for YouTube videos using the YouTube Data API.

    Args:
        query (str): Search query.
        max_results (int): Maximum number of results to return.
        api_key (str): YouTube API key.

    Returns:
        list: List of video details.
    """
    if not api_key:
        raise ValueError("YouTube API key is required.")

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoEmbeddable": "true",
        "maxResults": max_results,
        "key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])
        return [
            {
                "videoId": i["id"]["videoId"],
                "title": i["snippet"]["title"],
                "channel": i["snippet"]["channelTitle"],
                "thumbnail": i["snippet"]["thumbnails"]["high"]["url"],
            }
            for i in items
        ]
    except requests.exceptions.RequestException as e:
        st.error(f"YouTube API Error: {e}")
        return []


def get_youtube_video_details(video_id, api_key=None):
    """
    Get detailed information about a YouTube video.

    Args:
        video_id (str): YouTube video ID.
        api_key (str): YouTube API key.

    Returns:
        dict: Video details dictionary, or None if not found.
    """
    if not api_key:
        raise ValueError("YouTube API key is required.")

    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if "items" in data and data["items"]:
        item = data["items"][0]
        return {
            "title": item["snippet"].get("title"),
            "channel": item["snippet"].get("channelTitle"),
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
            "published": item["snippet"].get("publishedAt"),
            "duration": item["contentDetails"]["duration"],
        }
    return None


# Ensure YouTube audio analysis works correctly


def analyze_youtube_track(video_url, title="Track"):
    from pytube import YouTube
    import librosa

    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        if stream is None:
            raise ValueError("No downloadable stream found.")
        path = stream.download(
            output_path="app/audio", filename=f"{title.replace(' ', '_')}_temp.mp3"
        )

        y, sr = librosa.load(path, sr=None)
        bpm, key = detect_bpm_key(y, sr)
        mood = analyze_mood(path)
        energy = calculate_energy_profile(y)
        fig = generate_emotion_waveform(y, sr, mood, title)

        return {"bpm": bpm, "key": key, "energy": energy, "mood": mood, "fig": fig}
    except Exception as e:
        return {"error": str(e)}
