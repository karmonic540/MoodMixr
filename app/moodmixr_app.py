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
st.sidebar.title("🎛️ MoodMixr")
page = st.sidebar.radio("Navigate", ["Agent Analyzer"])

# 🧠 AGENT ANALYZER TAB
if page == "Agent Analyzer":
    LayoutAgent.page_header("🧠 Agent Analyzer")
    uploaded_files = st.file_uploader("🎵 Upload one or more track", 
                                      type=["mp3", "wav", "flac", "m4a"], 
                                      accept_multiple_files=True)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

    # Save uploaded files to /app/audio/
    uploaded_paths = []
    audio_dir = os.path.join(os.getcwd(), 'app', 'audio')
    os.makedirs(audio_dir, exist_ok=True)

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

    selected_display = st.selectbox("🎚️ Choose a track to analyze", track_info_display)
    selected_index = track_info_display.index(selected_display)
    selected_path = uploaded_paths[selected_index]

    # Dropdown to select a track (optional, can be removed if not needed)
    # selected_filename = st.selectbox("🎚️ Choose a track to analyze", [os.path.basename(p) for p in uploaded_paths])
    # selected_path = [p for p in uploaded_paths if selected_filename in p][0]

    with st.spinner("🔍 Running MoodMixr Agents..."):
        result = run_moodmixr_agent(selected_path)

    # Show player + art
    st.markdown("### 🎵 Preview Track")
    st.audio(selected_path)

    from utils.utils import extract_album_art, extract_track_metadata, get_mood_color
    art = extract_album_art(selected_path)
    meta = extract_track_metadata(selected_path)


    col1, col2 = st.columns([1, 3])
    with col1:
        if art:
            st.image(art, caption="Album Art", width=180)
    with col2:
        st.markdown(f"""
            <div style='margin-top:1rem'>
                <h4 style='margin-bottom:0;'>🎵 <b>{meta['title']}</b></h4>
                <p style='margin:0;'>👤 <b>{meta['artist']}</b></p>
                <p style='margin:0;'>💿 <b>{meta['album']}</b></p>
            </div>
        """, unsafe_allow_html=True)


    # Mood color
    mood_color = get_mood_color(result["Mood"])
    st.markdown(f"### 🎨 Mood: *{result['Mood']}*")
    st.markdown(f"<div style='height:20px; background-color:{mood_color}; border-radius:5px'></div>", unsafe_allow_html=True)


    # === WAVEFORM VISUALIZATION ===
    try:
        # Mood color + BPM-based glow speed
        bpm = result.get("BPM", 120)
        mood_color = get_mood_color(result["Mood"])
        glow_speed = (
            "1.2s" if bpm < 80 else
            "1s" if bpm < 110 else
            "0.8s" if bpm < 128 else
            "0.6s"
        )

        # Inject animated CSS glow for waveform
        st.markdown(f"""
        <style>
        @keyframes pulseGlow {{
            0%   {{ box-shadow: 0 0 10px {mood_color}33; }}
            100% {{ box-shadow: 0 0 25px {mood_color}CC; }}
        }}
        .glow-wave {{
            animation: pulseGlow {glow_speed} ease-in-out infinite alternate;
            border-radius: 12px;
            overflow: hidden;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }}
        </style>
        """, unsafe_allow_html=True)

        # Load waveform and render
        y, sr = librosa.load(selected_path)
        fig, ax = plt.subplots(figsize=(10, 3))

        librosa.display.waveshow(y, sr=sr, color=mood_color, alpha=0.85)
        ax.set_facecolor("#0D0D0D")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1, dpi=140, facecolor="#0D0D0D")
        plt.close(fig)

        st.markdown("### 🌊 Mood Waveform", unsafe_allow_html=True)
        st.markdown('<div class="glow-wave">', unsafe_allow_html=True)
        st.markdown('<div class="glow-wave">', unsafe_allow_html=True)
        st.image(Image.open(buf), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"Waveform error: {e}")



    # Metrics
    st.markdown("---")
    st.subheader("🎧 Track Intelligence")
    col1, col2, col3 = st.columns(3)
    col1.metric("🎚️ BPM", result['BPM'])
    col2.metric("🎼 Key", result['Key'])
    col3.metric("⚡ Energy", result['Energy'])

    st.markdown(f"#### 🎯 Set Role: *{result['SetRole']}*")
    st.markdown(f"#### 🎤 Vocals: {'Yes 🎙️' if result['HasVocals'] else 'No 🤐'} ({result['VocalConfidence']}% confidence)")
    st.markdown(f"#### 🧠 Summary: `{result['Summary']}`")

    st.markdown("#### 🔄 Transition Suggestions:")
    for suggestion in result["Suggestions"]:
        st.markdown(f"- {suggestion}")

    # Exported file
    export_filename = os.path.splitext(selected_display.split(' | ')[0])[0] + "_analysis.json"
    export_path = os.path.join("data", "exports", export_filename)
    if os.path.exists(export_path):
        with open(export_path, "rb") as f:
            st.download_button("📦 Download JSON", f, file_name=export_filename)
else:
    st.info("👆 Upload audio files to begin.")

    from utils.utils import extract_track_metadata
    from agents.set_optimizer_agent import SetOptimizerAgent


    # Initialize session state for DJ Set Queue
    if "dj_set_queue" not in st.session_state:
        st.session_state.dj_set_queue = []

    # --- DJ Set Preview Tab ---
    st.markdown("## 🎧 DJ Set Preview & Optimizer")

    uploaded_tracks = st.file_uploader("Upload your DJ tracks", type=["mp3", "wav", "flac"], accept_multiple_files=True)
    
    from utils.utils import detect_bpm_key, analyze_mood, calculate_energy_profile, extract_track_metadata

    if uploaded_tracks:
        new_files = [f.name for f in uploaded_tracks]
        existing_files = [t["file"].name for t in st.session_state.dj_set_queue]

        for file in uploaded_tracks:
            if file.name not in existing_files:
                # Save file
                temp_path = os.path.join("app", "audio", file.name)
                with open(temp_path, "wb") as f:
                    f.write(file.getbuffer())

                try:
                    # ANALYZE AUDIO
                    y, sr = librosa.load(temp_path, sr=None)
                    bpm, key = detect_bpm_key(y, sr)
                    energy = calculate_energy_profile(y)
                    mood = analyze_mood(temp_path)
                except Exception as e:
                    print(f"[AudioAnalysis] Failed: {e}")
                    bpm, key, energy, mood = "?", "?", 0.0, "Unknown"

                # METADATA
                metadata = extract_track_metadata(temp_path)
                filename_display = f"{metadata.get('artist', 'Unknown')} - {metadata.get('title', file.name)}"

                track_info = {
                    "name": metadata.get("title", file.name),
                    "artist": metadata.get("artist", "Unknown"),
                    "bpm": round(bpm) if isinstance(bpm, (int, float)) else "Detecting...",
                    "key": key or "Detecting...",
                    "mood": mood or "Analyzing...",
                    "energy": round(energy, 2),
                    "file": file,
                    "filename": filename_display
                }

                st.session_state.dj_set_queue.append(track_info)


    # Display Queue
    st.markdown("### 📋 Current Track Queue")

    if st.session_state.dj_set_queue:
        for i, track in enumerate(st.session_state.dj_set_queue):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"**{i+1}. {track['name']}** by *{track['artist']}*")
                st.caption(f"BPM: {track['bpm']} | Key: {track['key']} | Mood: {track['mood']}")
            with col2:
                if st.button("⬆️", key=f"up_{i}") and i > 0:
                    st.session_state.dj_set_queue[i], st.session_state.dj_set_queue[i - 1] = st.session_state.dj_set_queue[i - 1], st.session_state.dj_set_queue[i]
                if st.button("⬇️", key=f"down_{i}") and i < len(st.session_state.dj_set_queue) - 1:
                    st.session_state.dj_set_queue[i], st.session_state.dj_set_queue[i + 1] = st.session_state.dj_set_queue[i + 1], st.session_state.dj_set_queue[i]

        st.markdown("### 🧠 Optimize Set Flow")
        from utils.utils import generate_plotly_energy_curve
        st.markdown("### 🔋 Energy Flow Across Set")
        st.plotly_chart(generate_plotly_energy_curve(st.session_state.dj_set_queue), use_container_width=True)

        if st.button("🚀 Run Set Optimizer"):
            optimized_queue = SetOptimizerAgent.optimize_dj_set(st.session_state.dj_set_queue)
            st.session_state.dj_set_queue = optimized_queue
            st.success("Set flow optimized!")

    else:
        st.info("Upload some tracks to begin building your set!")


st.markdown("""
<div style='text-align:center; margin-top:3rem; font-size:13px; color:#BBBBBB'>
    ॐ नमः शिवाय — Let this DJ flow awaken your sound.<br>
    <span style='font-size:11px;'>Powered by MoodMixr · Built by Karmonic</span>
</div>
""", unsafe_allow_html=True)
