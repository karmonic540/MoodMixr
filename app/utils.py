# === utils.py ===
import librosa
import librosa.display
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cohere
import os
import streamlit as st

# Unified secret access: secrets.toml > fallback to env
def get_secret(key):
    return st.secrets.get(key) or os.getenv(key)

# BPM and Key Detection
def detect_bpm_key(y, sr):
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][np.argmax(np.mean(chroma, axis=1)) % 12]
    return int(tempo), key

# Mood Analysis via Cohere
def analyze_mood(audio_path):
    try:
        co = cohere.Client(get_secret("COHERE_API_KEY"))
        prompt = f"Analyze the mood of this audio track based on its name: {os.path.basename(audio_path)}"
        response = co.generate(model='command-light', prompt=prompt, max_tokens=20)
        return response.generations[0].text.strip()
    except Exception:
        return "Unknown / Neutral"

# Energy Calculation
def calculate_energy_profile(y):
    return float(np.mean(librosa.feature.rms(y=y)[0])) * 1000

# Mood Color
def get_mood_color(mood):
    mood = mood.lower()
    return {
        "happy": "#FF9900", "uplifting": "#FF9900", "calm": "#00CCFF", "chill": "#00CCFF",
        "dark": "#9900FF", "emotional": "#9900FF", "energetic": "#FF0033", "hype": "#FF0033"
    }.get(mood.split()[0], "#00FF99")

# BPM to Animation Speed
def get_bpm_animation_speed(bpm):
    return "1.2s" if bpm < 80 else "1s" if bpm < 100 else "0.8s" if bpm < 120 else "0.6s"

# Role Classifier
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

# Transition Suggestions
def suggest_best_transitions(track_data):
    def score(a, b):
        score = 100 - abs(a['bpm'] - b['bpm'])
        if a['key'] == b['key']: score += 15
        if a['mood'].split()[0].lower() in b['mood'].lower(): score += 10
        return score

    results = []
    for i, track in enumerate(track_data):
        best = max(
            (b for j, b in enumerate(track_data) if i != j),
            key=lambda b: score(track, b)
        )
        reason = f"Close BPM ({track['bpm']}→{best['bpm']}), "
        if track['key'] == best['key']: reason += "Key match ✅, "
        reason += "Similar mood 🎭" if track['mood'].split()[0].lower() in best['mood'].lower() else "Mood contrast"
        results.append({"from": track['filename'], "to": best['filename'], "score": score(track, best), "reason": reason})
    return results

# Plotly Energy Curve
import plotly.graph_objects as go
def generate_plotly_energy_curve(tracks):
    energies = [t["energy"] for t in tracks]
    labels = [t["filename"] for t in tracks]
    moods = [t["mood"] for t in tracks]
    colors = [get_mood_color(mood) for mood in moods]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(labels))), y=energies, mode='lines+markers',
                             marker=dict(size=12, color=colors), line=dict(color='white'),
                             text=labels, hoverinfo='text+y'))
    for i, label in enumerate(labels):
        fig.add_annotation(x=i, y=energies[i]+5, text=label[:20] + "...", showarrow=False,
                           font=dict(color=colors[i], size=12))
    fig.update_layout(title="🎚️ DJ Set Energy Flow", template="plotly_dark", height=400,
                      xaxis=dict(showticklabels=False), yaxis_title="Energy")
    return fig
