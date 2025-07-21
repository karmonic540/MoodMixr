# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause
import os
import sys
import io
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from mutagen import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from PIL import Image
from io import BytesIO


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from moodmixr_agent import run_moodmixr_agent
from agents.layout_agent import LayoutAgent



# 🎨 Streamlit Config
st.set_page_config(page_title="MoodMixr", layout="wide")
LayoutAgent.apply_global_styles()

# 🔧 Sidebar Navigation
st.sidebar.title("MoodMixr")
page = st.sidebar.radio("Navigate", ["Agent Analyzer", "Set Flow Designer"])

from utils.utils import (
    detect_bpm_key,
    analyze_mood,
    calculate_energy_profile,
    extract_album_art,
    extract_track_metadata,
    get_mood_color,
    generate_plotly_energy_curve
)
from agents.set_optimizer_agent import SetOptimizerAgent

# === AGENT ANALYZER TAB ===
if page == "Agent Analyzer":
    LayoutAgent.page_header("Agent Analyzer")

    uploaded_files = st.file_uploader(
        "Upload one or more track",
        type=["mp3", "wav", "flac", "m4a"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded")

        audio_dir = os.path.join(os.getcwd(), 'app', 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        uploaded_paths = []

        for uploaded_file in uploaded_files:
            file_path = os.path.join(audio_dir, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            uploaded_paths.append(file_path)

        track_info_display = []
        for path in uploaded_paths:
            try:
                f = sf.SoundFile(path)
                duration_sec = len(f) / f.samplerate
                minutes = int(duration_sec // 60)
                seconds = int(duration_sec % 60)
                size_mb = os.path.getsize(path) / (1024 * 1024)
                ext = os.path.splitext(path)[1][1:].upper()
                display = f"{os.path.basename(path)} | {minutes}m {seconds}s | {size_mb:.1f} MB | {ext}"
            except:
                display = os.path.basename(path)
            track_info_display.append(display)

        selected_display = st.selectbox("Choose a track to analyze", track_info_display)
        selected_index = track_info_display.index(selected_display)
        selected_path = uploaded_paths[selected_index]

        with st.spinner("Running MoodMixr Agents..."):
            result = run_moodmixr_agent(selected_path)

        st.markdown("### Preview Track")
        st.audio(selected_path)

        art = extract_album_art(selected_path)
        meta = extract_track_metadata(selected_path)

        col1, col2 = st.columns([1, 3])
        with col1:
            if art:
                st.image(art, caption="Album Art", width=180)
        with col2:
            st.markdown(f"""
                <h4>{meta['title']}</h4>
                <p>{meta['artist']} — {meta['album']}</p>
            """, unsafe_allow_html=True)

        mood_color = get_mood_color(result["Mood"])
        st.markdown(f"### Mood: *{result['Mood']}*")
        st.markdown(f"<div style='height:20px; background-color:{mood_color}; border-radius:5px'></div>", unsafe_allow_html=True)

        # === Waveform ===
        try:
            y, sr = librosa.load(selected_path)
            fig, ax = plt.subplots(figsize=(10, 3))
            librosa.display.waveshow(y, sr=sr, color=mood_color, alpha=0.85)
            ax.set_xticks([]), ax.set_yticks([]), ax.set_frame_on(False)
            for spine in ax.spines.values():
                spine.set_visible(False)
            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1, dpi=140)
            plt.close(fig)
            st.image(Image.open(buf), use_container_width=True)
        except Exception as e:
            st.warning(f"Waveform error: {e}")

        # === Results ===
        st.subheader("Track Intelligence")
        col1, col2, col3 = st.columns(3)
        col1.metric("BPM", result['BPM'])
        col2.metric("Key", result['Key'])
        col3.metric("Energy", result['Energy'])

        st.markdown(f"**Set Role**: *{result['SetRole']}*")
        st.markdown(f"**Vocals**: {'Yes' if result['HasVocals'] else 'No'} ({result['VocalConfidence']}%)")
        st.markdown(f"**Summary**: `{result['Summary']}`")

        st.markdown("**Transitions:**")
        for suggestion in result["Suggestions"]:
            st.markdown(f"- {suggestion}")

# === SET FLOW DESIGNER TAB ===
elif page == "Set Flow Designer":
    LayoutAgent.page_header("Set Flow Designer")

    if "dj_set_queue" not in st.session_state:
        st.session_state.dj_set_queue = []

    uploaded_tracks = st.file_uploader("Upload DJ set tracks", type=["mp3", "wav", "flac"], accept_multiple_files=True)

    if uploaded_tracks:
        new_files = [f.name for f in uploaded_tracks]
        existing_files = [t["file"].name for t in st.session_state.dj_set_queue]

        for file in uploaded_tracks:
            if file.name not in existing_files:
                temp_path = os.path.join("app", "audio", file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())

                try:
                    y, sr = librosa.load(temp_path, sr=None)
                    bpm, key = detect_bpm_key(y, sr)
                    energy = calculate_energy_profile(y)
                    mood = analyze_mood(temp_path)
                except Exception as e:
                    bpm, key, energy, mood = "?", "?", 0.0, "Unknown"

                metadata = extract_track_metadata(temp_path)
                track_info = {
                    "name": metadata.get("title", file.name),
                    "artist": metadata.get("artist", "Unknown"),
                    "bpm": round(bpm) if isinstance(bpm, (int, float)) else "Detecting...",
                    "key": key,
                    "mood": mood,
                    "energy": round(energy, 2),
                    "file": file,
                    "filename": file.name
                }
                st.session_state.dj_set_queue.append(track_info)

    if st.session_state.dj_set_queue:
        st.markdown("### Current Track Queue")

        for i, track in enumerate(st.session_state.dj_set_queue):
            with st.expander(f"{i+1}. {track['name']} by {track['artist']}"):
                st.caption(f"BPM: {track['bpm']} | Key: {track['key']} | Mood: {track['mood']}")
                st.audio(track["file"])

        st.markdown("### Optimize Set Flow")
        st.plotly_chart(generate_plotly_energy_curve(st.session_state.dj_set_queue), use_container_width=True)

        if st.button("Run Set Optimizer"):
            optimized_queue = SetOptimizerAgent.optimize_dj_set(st.session_state.dj_set_queue)
            st.session_state.dj_set_queue = optimized_queue
            st.success("Set flow optimized!")

    else:
        st.info("Upload some tracks to begin building your set.")

# === Footer ===
st.markdown("""
<div style='text-align:center; margin-top:3rem; font-size:13px; color:#BBBBBB'>
    ॐ नमः शिवाय — Let this DJ flow awaken your sound.<br>
    <span style='font-size:11px;'>Powered by MoodMixr · Built by Karmonic</span>
</div>
""", unsafe_allow_html=True)