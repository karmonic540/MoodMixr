import os
import sys
import io
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from mutagen import File as MutagenFile
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from PIL import Image
from io import BytesIO
from PIL import Image
import soundfile as sf
import soundfile as sf
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.utils import extract_album_art
from moodmixr_agent import run_moodmixr_agent

# 🎨 Streamlit Config
st.set_page_config(page_title="MoodMixr", layout="wide")

# 🔧 Sidebar Navigation
st.sidebar.title("🎛️ MoodMixr")
page = st.sidebar.radio("Navigate", ["Agent Analyzer"])

# 🧠 AGENT ANALYZER TAB
if page == "Agent Analyzer":
    st.title("🧠 Agent Analyzer")
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

    from utils.utils import extract_album_art
    art = extract_album_art(selected_path)
    if art:
        st.image(art, caption="Album Art", width=250)

    # Mood color
    from utils.utils import get_mood_color
    mood_color = get_mood_color(result["Mood"])
    st.markdown(f"### 🎨 Mood: *{result['Mood']}*")
    st.markdown(f"<div style='height:20px; background-color:{mood_color}; border-radius:5px'></div>", unsafe_allow_html=True)

    # Waveform
    try:
        import librosa
        import librosa.display
        import matplotlib.pyplot as plt
        import numpy as np
        from io import BytesIO
        from PIL import Image

        y, sr = librosa.load(selected_path)
        fig, ax = plt.subplots(figsize=(8, 2.5))
        librosa.display.waveshow(y, sr=sr, color=mood_color, alpha=0.9)
        ax.set_axis_off()
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.0)
        plt.close(fig)
        st.image(Image.open(buf), use_column_width=True)
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
