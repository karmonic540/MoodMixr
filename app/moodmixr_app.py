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
import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from PIL import Image
from io import BytesIO
import datetime
import concurrent.futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.layout_agent import LayoutAgent
from agents.vocal_detector_agent import VocalDetectorAgent
from agents.set_optimizer_agent import SetOptimizerAgent
from agents.transition_agent import TransitionRecommenderAgent
from utils.api_client import call_audio_agent_api, call_mood_agent_api
from utils.utils import (
    extract_album_art,
    extract_track_metadata,
    get_mood_color,
    generate_plotly_energy_curve,
)
from agents.summary_agent import SummaryAgent
from agents.genre_classifier_agent import GenreClassifierAgent

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# === Streamlit Config ===
st.set_page_config(page_title="MoodMixr", layout="wide")
LayoutAgent.apply_global_styles()
st.sidebar.title("MoodMixr")
page = st.sidebar.radio(
    "Navigate", ["Agent Analyzer", "Set Flow Designer", "Discover & Compare"]
)


# 🔁 Call Audio Agent via Docker (or local service)
def run_moodmixr_agent(track_path: str) -> dict:
    """Analyze a single track using Docker agents with graceful fallbacks."""
    # 1) AUDIO (BPM/Key) via HTTP agents
    audio_result = call_audio_agent_api(track_path)

    # accept both lower/upper-case keys and a common alias
    bpm_value = (
        audio_result.get("bpm")
        or audio_result.get("BPM")
        or audio_result.get("tempo")
        or 120.0
    )
    key_value = audio_result.get("key") or audio_result.get("Key")

    if bpm_value is None or key_value is None:
        st.error(f"❌ Audio Agent payload: {audio_result}")
        # ---- EMERGENCY LOCAL FALLBACK (no network / schema mismatch) ----
        try:
            # Adjust variable names for librosa
            y_audio, sr_audio = librosa.load(track_path, sr=None, mono=True)

            tempo, _ = librosa.beat.beat_track(y=y_audio, sr=sr_audio)
            bpm_value = float(tempo)

            chroma = librosa.feature.chroma_cqt(y=y_audio, sr=sr_audio).mean(axis=1)
            key_value = NOTE_NAMES[int(np.argmax(chroma))]
            st.warning("Used local fallback for BPM/Key.")
        except FileNotFoundError as e:
            st.error(f"File not found: {e}")
        except ValueError as e:
            st.error(f"Value error: {e}")
        except KeyError as e:
            st.error(f"Key error: {e}")
        except TypeError as e:
            st.error(f"Type error: {e}")
        except OSError as e:
            st.error(f"OS error: {e}")

    # Log the audio agent result for debugging
    st.write("Audio Agent Result:", audio_result)

    # Verify fallback mechanism
    if bpm_value is None or key_value is None:
        st.error("Fallback mechanism invoked.")
        st.write("Fallback BPM:", bpm_value)
        st.write("Fallback Key:", key_value)

    # 2) MOOD/ENERGY via HTTP agents
    mood_result = call_mood_agent_api(track_path)
    mood_value = (
        mood_result.get("mood")
        or mood_result.get("Mood")
        or mood_result.get("label")
        or "Unknown"
    )
    energy_value = (
        mood_result.get("energy")
        or mood_result.get("Energy")
        or mood_result.get("intensity")
        or 0.5
    )
    if energy_value is None:
        # keep app flowing even if agent omitted energy
        energy_value = 0.5

    # Log detailed agent responses for debugging
    st.write("Audio Agent Response:", audio_result)
    st.write("Mood Agent Response:", mood_result)

    # Ensure agent responses are correctly processed
    if not bpm_value:
        st.warning("Audio Agent did not return BPM. Defaulting to 0.")
        bpm_value = 0.0

    if not key_value:
        st.warning("Audio Agent did not return Key. Defaulting to 'Unknown'.")
        key_value = "Unknown"

    if not energy_value:
        st.warning("Mood Agent did not return Energy. Defaulting to 0.5.")
        energy_value = 0.5

    if not mood_value:
        st.warning("Mood Agent did not return Mood. Defaulting to 'Unknown'.")
        mood_value = "Unknown"

    # Debug agent responses
    st.write("Debugging Audio Agent Response:", audio_result)
    st.write("Debugging Mood Agent Response:", mood_result)

    # 3) Local helper agents (best-effort; never block)
    try:
        genre = GenreClassifierAgent.classify(track_path)
    except FileNotFoundError as e:
        genre = "Unknown"
        st.error(f"File not found: {e}")
    except ValueError as e:
        genre = "Unknown"
        st.error(f"Value error: {e}")
    except KeyError as e:
        genre = "Unknown"
        st.error(f"Key error: {e}")
    except TypeError as e:
        genre = "Unknown"
        st.error(f"Type error: {e}")
    except OSError as e:
        genre = "Unknown"
        st.error(f"OS error: {e}")

    try:
        vocals, confidence = VocalDetectorAgent.detect(track_path)
    except FileNotFoundError as e:
        vocals, confidence = False, 0.0
        st.error(f"File not found: {e}")
    except ValueError as e:
        vocals, confidence = False, 0.0
        st.error(f"Value error: {e}")
    except KeyError as e:
        vocals, confidence = False, 0.0
        st.error(f"Key error: {e}")
    except TypeError as e:
        vocals, confidence = False, 0.0
        st.error(f"Type error: {e}")
    except OSError as e:
        vocals, confidence = False, 0.0
        st.error(f"OS error: {e}")

    try:
        role = SetOptimizerAgent.classify_role(bpm_value, energy_value)
    except FileNotFoundError as e:
        role = "Support"
        st.error(f"File not found: {e}")
    except ValueError as e:
        role = "Support"
        st.error(f"Value error: {e}")
    except KeyError as e:
        role = "Support"
        st.error(f"Key error: {e}")
    except TypeError as e:
        role = "Support"
        st.error(f"Type error: {e}")
    except OSError as e:
        role = "Support"
        st.error(f"OS error: {e}")

    try:
        transitions = TransitionRecommenderAgent().recommend_adjacent_pairs(
            st.session_state.dj_set_queue
        )
    except FileNotFoundError as e:
        transitions = []
        st.error(f"File not found: {e}")
    except ValueError as e:
        transitions = []
        st.error(f"Value error: {e}")
    except KeyError as e:
        transitions = []
        st.error(f"Key error: {e}")
    except TypeError as e:
        transitions = []
        st.error(f"Type error: {e}")
    except OSError as e:
        transitions = []
        st.error(f"OS error: {e}")

    summary = SummaryAgent.generate_summary(
        filename=os.path.basename(track_path),
        bpm=bpm_value,
        key=key_value,
        mood=mood_value,
        set_role=role,
        has_vocals=vocals,
    )

    return {
        "Mood": mood_value,
        "Genre": genre,
        "HasVocals": vocals,
        "VocalConfidence": confidence,
        "Summary": summary,
        "BPM": bpm_value,
        "Key": key_value,
        "Energy": energy_value,
        "SetRole": role,
        "Suggestions": transitions,
    }


# === AGENT ANALYZER TAB ===
if page == "Agent Analyzer":
    LayoutAgent.page_header("Agent Analyzer")

    uploaded_files = st.file_uploader(
        "Upload one or more track",
        type=["mp3", "wav", "flac", "m4a"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded")

        audio_dir = os.path.join(os.getcwd(), "app", "audio")
        os.makedirs(audio_dir, exist_ok=True)
        uploaded_paths = []

        for uploaded_file in uploaded_files:
            file_path = os.path.join(audio_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
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
            except FileNotFoundError as e:
                display = os.path.basename(path)
                st.error(f"File not found: {e}")
            except ValueError as e:
                display = os.path.basename(path)
                st.error(f"Value error: {e}")
            except KeyError as e:
                display = os.path.basename(path)
                st.error(f"Key error: {e}")
            except TypeError as e:
                display = os.path.basename(path)
                st.error(f"Type error: {e}")
            except OSError as e:
                display = os.path.basename(path)
                st.error(f"OS error: {e}")

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
            st.markdown(
                f"""
                <h4>{meta['title']}</h4>
                <p>{meta['artist']} — {meta['album']}</p>
            """,
                unsafe_allow_html=True,
            )

        mood_color = get_mood_color(result["Mood"])
        st.markdown(f"### Mood: *{result['Mood']}*")
        st.markdown(
            f"<div style='height:20px; background-color:{mood_color}; border-radius:5px'></div>",
            unsafe_allow_html=True,
        )

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
            ax.set_title(
                "Waveform Energy Map", fontsize=14, color="white", pad=10, loc="center"
            )

            # Center-aligned Time label below waveform
            ax.text(
                0.5,
                -0.25,
                "Time",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=10,
                color="white",
                alpha=0.7,
            )

            # Hide borders
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Export
            buf = BytesIO()
            fig.savefig(
                buf,
                format="png",
                bbox_inches="tight",
                pad_inches=0.1,
                dpi=140,
                facecolor="#0D0D0D",
            )
            plt.close(fig)

            st.image(Image.open(buf), use_container_width=True)

        except (FileNotFoundError, OSError) as e:
            st.warning(f"Waveform error: {e}")
            st.error("Failed to generate waveform visualization.")

        # === Results ===
        st.subheader("Track Intelligence")
        col1, col2, col3 = st.columns(3)
        col1.metric("BPM", result["BPM"])
        col2.metric("Key", result["Key"])
        col3.metric("Energy", result["Energy"])

        st.markdown(f"**Set Role**: *{result['SetRole']}*")
        st.markdown(
            f"**Vocals**: {'Yes' if result['HasVocals'] else 'No'} ({result['VocalConfidence']}%)"
        )
        st.markdown(f"**Summary**: `{result['Summary']}`")

        st.markdown("**Transitions:**")
        for suggestion in result["Suggestions"]:
            st.markdown(f"- {suggestion}")

# === SET FLOW DESIGNER TAB ===
elif page == "Set Flow Designer":
    from utils.api_client import analyze_batch, ping_agents

    LayoutAgent.page_header("Set Flow Designer")

    if "dj_set_queue" not in st.session_state:
        st.session_state.dj_set_queue = []

    uploaded_tracks = st.file_uploader(
        "Upload DJ set tracks", type=["mp3", "wav", "flac"], accept_multiple_files=True
    )

    if uploaded_tracks:
        # Persist uploads to disk (agents read files)
        audio_dir = os.path.join("app", "audio")
        os.makedirs(audio_dir, exist_ok=True)

        new_paths = []
        for f in uploaded_tracks:
            temp_path = os.path.join(audio_dir, f.name)
            with open(temp_path, "wb") as out:
                out.write(f.getbuffer())
            new_paths.append(temp_path)

        # 🔁 Call both agents per track (Docker/local hybrid)
        from utils.api_client import analyze_batch, ping_agents

        ping = ping_agents()
        with st.expander("Agent status"):
            st.json(ping)

        # Prepare files and names for analyze_batch
        file_bytes = [f.getbuffer() for f in uploaded_tracks]
        file_names = [f.name for f in uploaded_tracks]

        with st.spinner("Analyzing tracks with MoodMixr agents..."):
            batch = analyze_batch(file_bytes, file_names)

        # Merge results into the session queue once per file
        existing_files = {t.get("filename") for t in st.session_state.dj_set_queue}

        # Prepare a working list of entries with merged fields and detect which need local fallback
        prepared = []
        for path, result in zip(new_paths, batch):
            filename = os.path.basename(path)
            if filename in existing_files:
                prepared.append(None)
                continue

            merged = result.get("merged") or {}

            bpm = merged.get("bpm")
            key = merged.get("key") or merged.get("Key")
            energy = merged.get("energy")
            mood = merged.get("mood")

            # Safe defaults
            bpm = (
                round(float(bpm))
                if isinstance(bpm, (int, float))
                else (0 if bpm is None else bpm)
            )
            key = key or "?"
            energy = (
                round(float(energy), 2) if isinstance(energy, (int, float)) else 0.5
            )
            mood = mood or "Unknown"

            prepared.append(
                {
                    "path": path,
                    "filename": filename,
                    "merged": merged,
                    "bpm": bpm,
                    "key": key,
                    "energy": energy,
                    "mood": mood,
                    "used_fallback": False,
                }
            )

        # Run local librosa fallbacks in parallel for entries that truly need it
        fallback_indices = [
            i
            for i, p in enumerate(prepared)
            if p
            and ((not p["bpm"] or p["bpm"] == 0.0) or (not p["key"] or p["key"] == "?"))
        ]

        def _compute_bpm_key(pth: str):
            try:
                y_local, sr_local = librosa.load(pth, sr=None, mono=True)
                tempo_local, _ = librosa.beat.beat_track(y=y_local, sr=sr_local)
                bpm_val = float(tempo_local) if tempo_local else None
                chroma_local = librosa.feature.chroma_cqt(y=y_local, sr=sr_local).mean(
                    axis=1
                )
                key_guess = NOTE_NAMES[int(np.argmax(chroma_local))]
                return bpm_val, key_guess
            except Exception:
                return None, None

        if fallback_indices:
            max_workers = min(4, (os.cpu_count() or 1))
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
                futures = {
                    ex.submit(_compute_bpm_key, prepared[i]["path"]): i
                    for i in fallback_indices
                }
                for fut in concurrent.futures.as_completed(futures):
                    i = futures[fut]
                    try:
                        bpm_val, key_guess = fut.result()
                        if bpm_val:
                            prepared[i]["bpm"] = float(bpm_val)
                        if key_guess and (
                            not prepared[i]["key"] or prepared[i]["key"] == "?"
                        ):
                            prepared[i]["key"] = key_guess
                        prepared[i]["used_fallback"] = bool(bpm_val or key_guess)
                        if prepared[i]["used_fallback"]:
                            st.warning(
                                f"Used local fallback for {prepared[i]['filename']}: BPM={prepared[i]['bpm']}, Key={prepared[i]['key']}"
                            )
                    except Exception as e:
                        st.info(
                            f"Local fallback failed for {prepared[i]['filename']}: {e}"
                        )

        # Now write debug files and append to session_state
        for p in prepared:
            if not p:
                continue

            path = p["path"]
            filename = p["filename"]
            bpm = p["bpm"]
            key = p["key"]
            energy = p["energy"]
            mood = p["mood"]
            used_fallback = p["used_fallback"]

            # Read tag metadata for nicer titles
            meta = extract_track_metadata(path)
            pretty_name = meta.get("title", filename)
            pretty_artist = meta.get("artist", "Unknown")

            track_info = {
                "name": pretty_name,
                "artist": pretty_artist,
                "bpm": bpm,
                "key": key,
                "mood": mood,
                "energy": energy,
                "file_path": path,
                "filename": filename,
            }

            # Dump per-file debug JSON to data/exports/debug/<filename>.json for inspection
            try:
                import json

                repo_root = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..")
                )
                debug_dir = os.path.join(repo_root, "data", "exports", "debug")
                os.makedirs(debug_dir, exist_ok=True)
                debug_path = os.path.join(debug_dir, f"{filename}.json")
                debug_entry = {
                    "filename": filename,
                    "used_fallback": used_fallback,
                    "merged": p.get("merged"),
                    "track_info": {
                        "name": track_info["name"],
                        "artist": track_info["artist"],
                        "bpm": track_info["bpm"],
                        "key": track_info["key"],
                        "mood": track_info["mood"],
                        "energy": track_info["energy"],
                    },
                }
                with open(debug_path, "w", encoding="utf-8") as df:
                    json.dump(debug_entry, df, indent=2)

                log_path = os.path.join(repo_root, "data", "exports", "debug_log.txt")
                with open(log_path, "a", encoding="utf-8") as lf:
                    lf.write(
                        f"{datetime.datetime.utcnow().isoformat()}\t{filename}\tused_fallback={used_fallback}\tbpm={track_info['bpm']}\tkey={track_info['key']}\n"
                    )

                with st.expander(f"Debug: {filename}"):
                    st.json(debug_entry)
            except Exception as e:
                st.warning(f"Could not write debug file for {filename}: {e}")

            st.session_state.dj_set_queue.append(track_info)

    # DJ Set Queue
    if st.session_state.dj_set_queue:
        st.subheader("Current DJ Set Queue")
        # Allow user to optimize the set order using the SetOptimizerAgent
        if st.button("Optimize set order"):
            try:
                optimized = SetOptimizerAgent.optimize_dj_set(
                    st.session_state.dj_set_queue
                )
                st.session_state.dj_set_queue = optimized
                st.success("Set optimized — order updated.")
            except Exception as e:
                st.warning(f"Optimization failed: {e}")
        for track in st.session_state.dj_set_queue:
            st.write(
                f"- {track['name']} by {track['artist']} (BPM: {track['bpm']}, Key: {track['key']})"
            )

        with st.expander("Set Flow Visualization"):
            # Generate and display the energy curve for the current set
            try:
                fig = generate_plotly_energy_curve(st.session_state.dj_set_queue)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not generate energy curve: {e}")

            # === TRANSITION SUGGESTIONS ===
            st.subheader("Transition Suggestions")
            if len(st.session_state.dj_set_queue) < 2:
                st.info("Add more tracks to see transition suggestions.")
            else:
                # Extract only the necessary data for transitions
                simplified_queue = [
                    {
                        "name": t["name"],
                        "artist": t["artist"],
                        "bpm": t["bpm"],
                        "key": t["key"],
                    }
                    for t in st.session_state.dj_set_queue
                ]

                # Generate transitions using the latest agent
                try:
                    # The agent returns a list of dicts like {from,to,score,reasons,strategy}
                    transitions = TransitionRecommenderAgent().recommend_adjacent_pairs(
                        simplified_queue
                    )
                    for t in transitions:
                        frm = t.get("from") or t.get("from_name") or "Unknown"
                        to = t.get("to") or "Unknown"
                        score = t.get("score")
                        strategy = t.get("strategy")
                        reasons = t.get("reasons") or []
                        st.write(f"- **{frm}** ➔ **{to}**  (score: {score})")
                        if strategy:
                            st.caption(
                                f"Strategy: {strategy} — Reasons: {', '.join(reasons)}"
                            )
                except Exception as e:
                    st.warning(f"Could not generate transitions: {e}")

    else:
        st.info("Upload tracks to get started with your DJ set.")
