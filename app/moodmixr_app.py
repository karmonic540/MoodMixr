import streamlit as st
import librosa
import os
import numpy as np
import streamlit.components.v1 as components
from utils import (
    detect_bpm_key,
    analyze_mood,
    calculate_energy_profile,
    generate_plotly_energy_curve,
    get_bpm_animation_speed,
    get_mood_color,
    suggest_best_transitions
)

# 🎨 Global Style
st.markdown("""
<style>
body {
    background-color: #0D0D0D;
}
h1, h2, h3, h4 {
    color: #FF00FF;
}
.stMarkdown {
    font-family: 'Segoe UI', sans-serif;
    padding: 1rem;
    margin-bottom: 1rem;
    background: #111111;
    border-radius: 10px;
    border: 1px solid #333333;
}
.metric-container > div {
    background-color: #111111;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #333333;
}
</style>
""", unsafe_allow_html=True)

# 🎧 MoodMixr Title
st.markdown("<h1 style='text-align: center; color: #FF00FF;'>🎧 MoodMixr</h1>", unsafe_allow_html=True)
st.caption("AI-powered DJ Insight Tool for Pros")

tab1, tab2 = st.tabs(["🎵 Single Track Analyzer", "🚀 DJ Set Optimizer"])

# ========== TAB 1 ==========
with tab1:
    st.markdown("### 🎯 Track Analyzer")

    uploaded_file = st.file_uploader("Upload an audio file (.mp3 or .wav)", type=["mp3", "wav"])
    if uploaded_file is not None:
        audio_path = os.path.join("app/audio", uploaded_file.name)
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.read())

        st.audio(audio_path)

        y, sr = librosa.load(audio_path, sr=None)
        duration = librosa.get_duration(y=y, sr=sr)
        bpm, key = detect_bpm_key(y, sr)
        mood = analyze_mood(audio_path)

        # 🎚️ Metrics
        with st.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("⏱️ BPM", bpm)
            col2.metric("🎼 Key", key)
            col3.metric("🧠 Mood", mood.split()[0])

        # 🎛️ EQ Visualizer (Multi-color, Staggered Animation)
        eq_colors = [
            "#FF007F", "#00FFFF", "#FF9900", "#7FFF00", "#FF0033",
            "#00FF99", "#9900FF", "#FFCC00", "#00CCFF", "#FF00FF"
        ]
        color = get_mood_color(mood)
        speed = get_bpm_animation_speed(bpm)

        bars = "".join([
            f'''
            <div style="flex: 1; height: {40 + (i % 4) * 10}px;
                        background: {eq_colors[i % len(eq_colors)]};
                        animation: bounce {0.3 + (i % 5) * 0.1}s infinite alternate;"></div>
            '''
            for i in range(20)
        ])

        eq_html = f'''
        <div style="width: 100%; height: 80px; display: flex;
                    justify-content: space-between;
                    align-items: flex-end; margin-top: 25px;">
            {bars}
        </div>
        <style>
        @keyframes bounce {{
            0% {{ transform: scaleY(1); }}
            100% {{ transform: scaleY(2); }}
        }}
        </style>
        '''
        components.html(eq_html, height=100)

# ========== TAB 2 ==========
with tab2:
    st.markdown("### 🎚️ DJ Set Optimizer")

    uploaded_files = st.file_uploader("Upload multiple files", type=["mp3", "wav"], accept_multiple_files=True)
    if uploaded_files:
        track_data = []

        for file in uploaded_files:
            file_path = os.path.join("app/audio", file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())

            y, sr = librosa.load(file_path, sr=None)
            bpm, key = detect_bpm_key(y, sr)
            mood = analyze_mood(file_path)
            energy = calculate_energy_profile(y)

            track_data.append({
                "filename": file.name,
                "bpm": bpm,
                "key": key,
                "mood": mood,
                "energy": energy
            })

        sorted_tracks = sorted(track_data, key=lambda x: x["energy"])

        for i, track in enumerate(sorted_tracks):
            st.markdown(f"**{i+1}.** `{track['filename']}` | BPM: {track['bpm']} | Energy: {track['energy']:.2f} | Mood: {track['mood']}")

        plotly_chart = generate_plotly_energy_curve(sorted_tracks)
        st.plotly_chart(plotly_chart, use_container_width=True)

        st.markdown("### 🔀 AI-Suggested Transitions")
        transitions = suggest_best_transitions(sorted_tracks)
        for t in transitions:
            st.markdown(f"🎧 Best next track after **`{t['from']}`** → **`{t['to']}`**  \n_Reason: {t['reason']}_")
