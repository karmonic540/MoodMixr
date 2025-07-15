# === moodmixr_app.py ===
import streamlit as st
import os
import librosa
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

from utils import (
    detect_bpm_key, analyze_mood, calculate_energy_profile,
    generate_plotly_energy_curve, get_bpm_animation_speed,
    get_mood_color, suggest_best_transitions, classify_set_role
)

st.set_page_config(page_title="MoodMixr", layout="wide")
st.markdown("""
<style>
body { background-color: #0D0D0D; }
h1, h2, h3, h4 { color: #FF00FF; }
.metric-container > div {
    background-color: #111111;
    border-radius: 12px;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #333333;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FF00FF;'>🎧 MoodMixr</h1>", unsafe_allow_html=True)
st.caption("AI-powered DJ Insight Tool for Pros")

tab1, tab2 = st.tabs(["🎵 Single Track Analyzer", "🚀 DJ Set Optimizer"])

# === TAB 1 ===
with tab1:
    st.markdown("### 🎯 Track Analyzer")
    file = st.file_uploader("Upload a track (.mp3/.wav)", type=["mp3", "wav"])
    if file:
        path = f"app/audio/{file.name}"
        with open(path, "wb") as f: f.write(file.read())
        st.audio(path)
        y, sr = librosa.load(path, sr=None)
        bpm, key = detect_bpm_key(y, sr)
        mood = analyze_mood(path)

        col1, col2, col3 = st.columns(3)
        col1.metric("⏱️ BPM", bpm)
        col2.metric("🎼 Key", key)
        col3.metric("🧠 Mood", mood.split()[0])

        bars = "".join([
            f"<div style='flex:1; height:{40+(i%4)*10}px; background:{get_mood_color(mood)}; animation:bounce {0.3+(i%5)*0.1}s infinite alternate;'></div>"
            for i in range(200)
        ])
        eq_html = f"<div style='display:flex; justify-content:space-between; align-items:flex-end; height:80px;'>{bars}</div><style>@keyframes bounce{{0%{{transform:scaleY(1);}}100%{{transform:scaleY(2);}}}}</style>"
        components.html(eq_html, height=100)

# === TAB 2 ===
with tab2:
    st.markdown("### 🎚️ DJ Set Optimizer")
    files = st.file_uploader("Upload multiple files", type=["mp3", "wav"], accept_multiple_files=True)

    if files:
        tracks = []
        for f in files:
            path = f"app/audio/{f.name}"
            with open(path, "wb") as out: out.write(f.read())
            y, sr = librosa.load(path, sr=None)
            bpm, key = detect_bpm_key(y, sr)
            mood = analyze_mood(path)
            energy = calculate_energy_profile(y)
            tracks.append({"filename": f.name, "bpm": bpm, "key": key, "mood": mood, "energy": energy})

        tracks = sorted(tracks, key=lambda x: x["energy"])
        for t in tracks:
            t["role"] = classify_set_role(t["bpm"], t["energy"], t["mood"])

        for t in tracks:
            st.markdown(f"""
            <div style='padding:15px; border-left:5px solid {get_mood_color(t['mood'])}; background:#1a1a1a; border-radius:10px; margin-bottom:15px;'>
                <h4 style='color:{get_mood_color(t['mood'])};'>{t['role']}</h4>
                <b>{t['filename']}</b><br>
                <span>BPM: {t['bpm']} | Key: {t['key']} | Energy: {t['energy']:.2f}</span><br>
                <i style='color:#bbb;'>Mood: {t['mood']}</i>
            </div>""", unsafe_allow_html=True)

        df = pd.DataFrame(tracks)[["filename", "bpm", "key", "mood", "energy"]]
        st.download_button("📥 Download CSV", df.to_csv(index=False).encode(), "dj_set.csv", "text/csv")

        st.markdown("### 🔗 Transition Suggestions")
        for t in suggest_best_transitions(tracks):
            st.markdown(f"<div style='padding:10px; background:#111; margin:10px 0; border-left:4px solid #FF00FF;'><b>{t['from']} ➜ {t['to']}</b><br><small>{t['reason']}</small></div>", unsafe_allow_html=True)

        st.markdown("### 📊 Energy Curve")
        st.plotly_chart(generate_plotly_energy_curve(tracks), use_container_width=True)

        st.markdown("### 🤖 Ask MoodMixr AI")
        query = st.text_input("Ask about your set (e.g., 'Suggest 3-track opener')")
        if query:
            import cohere
            co = cohere.Client(st.secrets["COHERE_API_KEY"])
            context = "\n".join([f"{t['filename']} | BPM: {t['bpm']} | Key: {t['key']} | Mood: {t['mood']} | Energy: {t['energy']:.2f}" for t in tracks])
            prompt = f"You are a pro DJ assistant in MoodMixr.\nTracklist:\n{context}\n\nUser query: {query}\nRespond concisely:"
            result = co.generate(model="command-light", prompt=prompt, max_tokens=100)
            st.success(result.generations[0].text.strip())
