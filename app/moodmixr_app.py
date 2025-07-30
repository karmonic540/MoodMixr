# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause
# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause

# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 AI + Human Creativity | 🎵 Modular DJ Intelligence
# 🧠 Agent-Based Architecture | Version 0.9.5

import os
import sys
import io
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from PIL import Image
from io import BytesIO


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from agents.layout_agent import LayoutAgent
from agents.audio_agent import AudioAnalyzerAgent
from agents.mood_agent import MoodClassifierAgent as MoodAgent
from agents.genre_classifier_agent import GenreClassifierAgent
from agents.vocal_detector_agent import VocalDetectorAgent
from agents.set_optimizer_agent import SetOptimizerAgent
from agents.transition_agent import TransitionRecommenderAgent
from agents.summary_agent import SummaryAgent
from agents.discover_agent import DiscoverAgent
from utils.utils import extract_album_art, extract_track_metadata, generate_plotly_energy_curve, get_mood_color

# === Streamlit Config ===
st.set_page_config(page_title="MoodMixr", layout="wide")
LayoutAgent.apply_global_styles()
st.sidebar.title("MoodMixr")
page = st.sidebar.radio("Navigate", ["Agent Analyzer", "Set Flow Designer", "Discover & Compare"])

# === Central Execution ===
def run_moodmixr_agent(track_path):
    bpm, key = AudioAnalyzerAgent.analyze(track_path)
    mood, energy = MoodAgent.analyze(track_path)
    genre = GenreClassifierAgent.classify(track_path)
    vocals, confidence = VocalDetectorAgent.detect(track_path)
    role = SetOptimizerAgent.classify_role(bpm, energy)
    transitions = TransitionRecommenderAgent.recommend(bpm=bpm, key=key, mood=mood, energy=energy)
    summary = SummaryAgent.generate_summary(
        filename=os.path.basename(track_path),
        bpm=bpm,
        key=key,
        mood=mood,
        set_role=role,
        has_vocals=vocals
    )
    return {
        "Mood": mood,
        "Genre": genre,
        "HasVocals": vocals,
        "VocalConfidence": confidence,
        "Summary": summary,
        "BPM": bpm,
        "Key": key,
        "Energy": energy,
        "SetRole": role,
        "Suggestions": transitions
    }

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

        # === WAVEFORM VISUALIZATION ===
        try:
            y, sr = librosa.load(selected_path)
            fig, ax = plt.subplots(figsize=(10, 3), facecolor="#0D0D0D")

            librosa.display.waveshow(y, sr=sr, color=mood_color, alpha=0.85)

            # === Styling ===
            ax.set_facecolor("#0D0D0D")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(False)

            # Title above waveform
            ax.set_title("Waveform Energy Map", fontsize=14, color="white", pad=10, loc="center")

            # Center-aligned Time label below waveform
            ax.text(0.5, -0.25, 'Time', ha='center', va='center', transform=ax.transAxes,
                    fontsize=10, color='white', alpha=0.7)

            # Hide borders
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Export
            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1, dpi=140, facecolor="#0D0D0D")
            plt.close(fig)

            st.image(Image.open(buf), use_container_width=True)

        except Exception as e:
            st.warning(f"Waveform error: {e}")
            st.error("Failed to generate waveform visualization.")


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
    from agents.audio_agent import AudioAnalyzerAgent
    from agents.mood_agent import MoodClassifierAgent
    from agents.genre_classifier_agent import GenreClassifierAgent
    from agents.set_optimizer_agent import SetOptimizerAgent
    from agents.transition_agent import TransitionRecommenderAgent

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
                    bpm, key = AudioAnalyzerAgent.analyze(temp_path)
                    mood, energy = MoodClassifierAgent.analyze(temp_path)
                    mood = mood.strip().strip('"').strip(",").capitalize()
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

        st.markdown("<a href='#dj-energy' style='text-decoration:none;'>🔽 View Energy Map</a>", unsafe_allow_html=True)

    if st.session_state.dj_set_queue:
        st.markdown("### Current Track Queue")
        for i, track in enumerate(st.session_state.dj_set_queue):
            col1, col2 = st.columns([8, 1])
            with col1:
                with st.expander(f"{i+1}. {track['name']} by {track['artist']}"):
                    st.caption(f"BPM: {track['bpm']} | Key: {track['key']} | Mood: {track['mood']}")
                    st.audio(track["file"])
            with col2:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.dj_set_queue.pop(i)
                    st.experimental_rerun()

        st.markdown("---")
        st.markdown("<h4 id='dj-energy'>Energy Flow</h4>", unsafe_allow_html=True)
        st.plotly_chart(generate_plotly_energy_curve(st.session_state.dj_set_queue), use_container_width=True)

        st.markdown("---")
        st.markdown("### Transition Insights")
        for i, track in enumerate(st.session_state.dj_set_queue):
            with st.expander(f"{i+1}. {track['name']} by {track['artist']}"):
                st.caption(f"BPM: {track['bpm']} | Key: {track['key']} | Mood: {track['mood']}")
                st.audio(track["file"])
                try:
                    bpm = float(track['bpm']) if isinstance(track['bpm'], (int, float)) else 120
                    energy = float(track['energy']) if isinstance(track['energy'], (int, float)) else 0.5
                    mood = str(track['mood']) or "Neutral"
                    key = str(track['key']) or "C"

                    suggestions = TransitionRecommenderAgent.recommend(
                        bpm=bpm,
                        key=key,
                        mood=mood,
                        energy=energy
                    )
                    st.markdown("**Suggestions:**")
                    for s in suggestions:
                        st.markdown(f"<div style='background-color:#1E1E1E; padding:5px 10px; border-radius:6px; margin-bottom:5px; color:#BBB;'>{s}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Could not generate transitions: {e}")

        # === OPTIMIZER ===
        st.markdown("---")
        if st.button("Run Set Optimizer"):
            optimized_queue = SetOptimizerAgent.optimize_dj_set(st.session_state.dj_set_queue)
            st.session_state.dj_set_queue = optimized_queue
            st.success("Set flow optimized!")

        # === SET SUMMARY DISPLAY ===
        st.markdown("---")
        st.subheader("📜 Set Summary View")

        for i, track in enumerate(st.session_state.dj_set_queue):
            filename = track.get("filename", f"Track {i+1}")
            bpm = track.get("bpm", "?")
            key = track.get("key", "?")
            mood = track.get("mood", "Unknown")
            energy = track.get("energy", "?")
            set_role = track.get("SetRole", "🎚️ Support")
            has_vocals = track.get("HasVocals", False)

            # 💡 Generate the AI-powered summary
            ai_summary = SummaryAgent.generate_summary(filename, bpm, key, mood, set_role, has_vocals)

            st.markdown(f"""
            <div style='background-color:#111111; padding:10px 15px; border-radius:10px; margin-bottom:10px;'>
                <h4 style='color:#00FF99;'>🎵 {i+1}. {track['name']} <span style='color:#999;'>by {track['artist']}</span></h4>
                <p style='margin:0;'>
                    <b>BPM:</b> {bpm} &nbsp; | &nbsp;
                    <b>Key:</b> {key} &nbsp; | &nbsp;
                    <b>Energy:</b> {energy} &nbsp; | &nbsp;
                    <b>Mood:</b> {mood}
                </p>
                <p style='color:#AAA; font-style:italic; margin-top:10px;'>{ai_summary}</p>
            </div>
            """, unsafe_allow_html=True)

        # === EXPORT OPTION ===
        summary_text = "\n".join([
            SummaryAgent.generate_summary(
                t.get("filename", f"Track {i+1}"),
                t.get("bpm", "?"),
                t.get("key", "?"),
                t.get("mood", "Unknown"),
                t.get("SetRole", "🎚️ Support"),
                t.get("HasVocals", False)
            ) for i, t in enumerate(st.session_state.dj_set_queue)
        ])

        st.download_button("📥 Export Set Summary (TXT)", summary_text, file_name="moodmixr_dj_set_summary.txt")

        # === EXPORT TO JSON ===
        import json
        export_data = [
            {
                "order": i+1,
                "name": t["name"],
                "artist": t["artist"],
                "bpm": t["bpm"],
                "key": t["key"],
                "mood": t["mood"],
                "energy": t["energy"]
            } for i, t in enumerate(st.session_state.dj_set_queue)
        ]
        export_json = json.dumps(export_data, indent=4)
        st.download_button("Export DJ Set (JSON)", export_json, file_name="dj_set_export.json")

    else:
        st.info("Upload some tracks to begin building your set.")

# === DISCOVER & COMPARE TAB ===

elif page == "Discover & Compare":
    from moodmixr_agent import run_discover_agent

    LayoutAgent.page_header("Discover & Compare")
    st.subheader(" Discover Tracks on Spotify")

    query = st.text_input("Search Spotify", placeholder="Try 'Sunset Lover', 'Fred Again..', etc.")
    use_youtube_fallback = st.sidebar.checkbox("🎵 Use YouTube fallback if Spotify preview fails", value=True)
    results_per_page = 10

    # Init session state
    if query:
        if "discover_query" not in st.session_state:
            st.session_state.discover_query = ""
        if "discover_index" not in st.session_state:
            st.session_state.discover_index = 0
        if "discover_results" not in st.session_state:
            st.session_state.discover_results = []

        # Reset if new query
        if st.session_state.discover_query != query:
            st.session_state.discover_query = query
            st.session_state.discover_results = []
            st.session_state.discover_index = 0

        # Load next results
        new_results = run_discover_agent(query, st.session_state.discover_index, results_per_page,use_youtube_fallback=use_youtube_fallback)
        st.session_state.discover_results += new_results
        st.session_state.discover_index += results_per_page

        # Filters
        st.markdown("### 🔍 Filters")
        show_only_preview = st.checkbox("Only show tracks with preview", value=False)
        with st.expander("🎛️ Filter by BPM & Energy"):
            bpm_range = st.slider("BPM", 60, 200, (60, 200))
            energy_range = st.slider("Energy", 0.0, 1.0, (0.0, 1.0), step=0.05)

        # Robust filter logic
        results_to_show = []
        for t in st.session_state.discover_results:
            has_valid_bpm = isinstance(t["bpm"], (int, float)) and t["bpm"] > 0
            has_valid_energy = isinstance(t["energy"], (int, float)) and t["energy"] > 0

            if show_only_preview and not t.get("preview_url"):
                continue
            if has_valid_bpm and not (bpm_range[0] <= t["bpm"] <= bpm_range[1]):
                continue
            if has_valid_energy and not (energy_range[0] <= t["energy"] <= energy_range[1]):
                continue

            results_to_show.append(t)

        # Display tracks
        for track in results_to_show:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(track["image"], width=100)
            with col2:
                st.markdown(f"**{track['name']}** by *{track['artist']}*")
                st.markdown(f"<span style='color: #00ff99'>Album:</span> {track['album']}", unsafe_allow_html=True)
                st.markdown(
                    f"<span style='color: #CCCCCC'>BPM:</span> <b>{track['bpm']}</b> &nbsp; "
                    f"<span style='color: #CCCCCC'>Key:</span> <b>{track['key']}</b> &nbsp; "
                    f"<span style='color: #CCCCCC'>Energy:</span> <b>{track['energy']}</b> &nbsp; "
                    f"<span style='color: #CCCCCC'>Mood:</span> <b>{track['mood']}</b><br> "
                    f"<span style='color: #888888; font-size: 11px;'>(via {track.get('source', 'Unknown')})</span>",

                    unsafe_allow_html=True
                )
                if track.get("preview_url"):
                    st.audio(track["preview_url"], format="audio/mp3")
                else:
                    st.components.v1.html(
                        f"""<iframe style="border-radius:12px" 
                            src="https://open.spotify.com/embed/track/{track['id']}" 
                            width="100%" height="80" frameBorder="0" allowtransparency="true" allow="encrypted-media">
                        </iframe>""",
                        height=100
                    )

            if st.button(" Add to Set", key=f"add_{track['id']}"):
                if "dj_set_queue" not in st.session_state:
                    st.session_state.dj_set_queue = []
                st.session_state.dj_set_queue.append({
                    "name": track["name"],
                    "artist": track["artist"],
                    "bpm": track["bpm"],
                    "key": track["key"],
                    "mood": track["mood"],
                    "energy": track["energy"],
                    "file": None,
                    "filename": f"{track['name']} (Spotify)"
                })
                st.success(f" Added '{track['name']}' to your DJ set.")

        # Load more
        st.markdown("---")
        if st.button("Load More"):
            st.rerun()



# === Footer ===
st.markdown("""
<div style='text-align:center; margin-top:3rem; font-size:13px; color:#BBBBBB'>
    ॐ नमः शिवाय — Let this DJ flow awaken your sound.<br>
    <span style='font-size:11px;'>Powered by MoodMixr · Built by Karmonic</span>
</div>
""", unsafe_allow_html=True)