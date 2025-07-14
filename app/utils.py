
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import cohere
import os

# Detect BPM and Key
def detect_bpm_key(y, sr):
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)
    key_index = chroma_mean.argmax()
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = keys[key_index % 12]
    return int(tempo), key

# Generate waveform visualization with emotion-inspired color
def generate_waveform(y, sr):
    fig, ax = plt.subplots(figsize=(10, 3))
    librosa.display.waveshow(y, sr=sr, alpha=0.8, ax=ax, color='#ff4c8b')
    ax.set_title('Waveform')
    ax.set_xlabel('')
    ax.set_yticks([])
    ax.set_xticks([])
    plt.tight_layout()
    return fig

# Placeholder AI mood analysis (using Cohere or fallback)
def analyze_mood(audio_path):
    try:
        co = cohere.Client(os.getenv("COHERE_API_KEY"))  # Set this in your .env or Streamlit Secrets
        prompt = f"Analyze the mood of this audio track based on its name: {os.path.basename(audio_path)}"
        response = co.generate(
            model='command-light',
            prompt=prompt,
            max_tokens=20
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return "Unknown / Neutral"


# Calculate energy level of an audio track using Root Mean Square (RMS)
def calculate_energy_profile(y):
    rms = librosa.feature.rms(y=y)[0]
    energy = float(np.mean(rms)) * 1000  # Scale for readability
    return energy

import plotly.graph_objects as go

def get_mood_color(mood):
    mood = mood.lower()
    if "happy" in mood or "uplifting" in mood:
        return "#FF9900"  # warm orange
    elif "calm" in mood or "chill" in mood:
        return "#00CCFF"  # light blue
    elif "dark" in mood or "emotional" in mood:
        return "#9900FF"  # deep purple
    elif "energetic" in mood or "hype" in mood:
        return "#FF0033"  # red
    else:
        return "#00FF99"  # neutral green-blue

def generate_plotly_energy_curve(sorted_tracks):
    import plotly.graph_objects as go

    energies = [t["energy"] for t in sorted_tracks]
    labels = [t["filename"] for t in sorted_tracks]
    moods = [t["mood"] for t in sorted_tracks]
    colors = [get_mood_color(mood) for mood in moods]

    fig = go.Figure()

    # Dots + line
    fig.add_trace(go.Scatter(
        x=list(range(len(labels))),
        y=energies,
        mode='lines+markers',
        marker=dict(size=12, color=colors),
        line=dict(color='white', width=2),
        text=labels,
        hoverinfo='text+y'
    ))

    # Add track names above each point
    for i, label in enumerate(labels):
        fig.add_annotation(
            x=i,
            y=energies[i] + 5,
            text=label.split(".mp3")[0][:25] + "...",
            showarrow=False,
            font=dict(color=colors[i], size=12)
        )

    fig.update_layout(
        title="🎚️ DJ Set Energy Flow (MoodMixr AI)",
        xaxis=dict(showticklabels=False),  # hide x-axis labels
        yaxis_title="Energy",
        template="plotly_dark",
        height=400
    )

    return fig


def get_bpm_animation_speed(bpm):
    if bpm < 80:
        return "1.2s"
    elif bpm < 100:
        return "1s"
    elif bpm < 120:
        return "0.8s"
    else:
        return "0.6s"
def suggest_best_transitions(track_data):
    def score_transition(track_a, track_b):
        bpm_diff = abs(track_a['bpm'] - track_b['bpm'])
        key_match = track_a['key'] == track_b['key']
        mood_similar = track_a['mood'].split()[0].lower() in track_b['mood'].lower()

        score = 100 - bpm_diff
        if key_match:
            score += 15
        if mood_similar:
            score += 10
        return score

    transitions = []
    for i, current in enumerate(track_data):
        best_score = -1
        best_next = None
        reason = ""
        for j, candidate in enumerate(track_data):
            if i == j:
                continue
            score = score_transition(current, candidate)
            if score > best_score:
                best_score = score
                best_next = candidate
                bpm_diff = abs(current['bpm'] - candidate['bpm'])
                reason = f"Close BPM ({current['bpm']} → {candidate['bpm']}), " + \
                         ("Key match ✅, " if current['key'] == candidate['key'] else "") + \
                         ("Similar mood 🎭" if current['mood'].split()[0].lower() in candidate['mood'].lower() else "Mood contrast")

        transitions.append({
            "from": current['filename'],
            "to": best_next['filename'],
            "score": best_score,
            "reason": reason
        })

    return transitions
