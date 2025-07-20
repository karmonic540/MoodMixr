import streamlit as st
import os
import sys
import librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64
from pytube import YouTube
from ytmusicapi import YTMusic
from utils import (
    detect_bpm_key,
    analyze_mood,
    calculate_energy_profile,
    generate_emotion_waveform,
    generate_plotly_energy_curve,
    get_bpm_animation_speed,
    get_mood_color,
    suggest_best_transitions,
    get_spotify_token,
    classify_set_role,
    search_youtube_videos,
    get_youtube_video_details
)

# Ensure audio dir
os.makedirs("app/audio", exist_ok=True)
yt = YTMusic()


# === GLOBAL THEME ===
st.set_page_config(page_title="MoodMixr", layout="wide")

st.markdown("""
<style>
body, .stApp {
    background-color: #0e0e0e;
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}

.mood-box {
    height: 160px; /* Ensure consistent height */
    overflow: hidden;
    background: #1a1a1a;
    border-left: 6px solid var(--mood-color, #FF00FF);
    border-radius: 10px;
    padding: 15px 20px;
    margin-top: 25px;
    box-shadow: 0 0 8px var(--mood-color-glow, #ff00ff44);
}

.mood-box h4 {
    margin-bottom: 8px;
    color: var(--mood-color, #FF00FF);
}

.mood-box p {
    margin: 0;
    font-size: 1.05rem;
    color: white;
    line-height: 1.4;
}

.spacer {
    height: 24px; /* Add space between mood box and waveform */
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FF00FF;'>🎧 MoodMixr</h1>", unsafe_allow_html=True)
st.caption("AI-powered DJ Insight Tool for Pros")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Track Analyzer", "DJ Set Optimizer", "Performance Mode",
    "📚 Library Insight", "🎯 Discovery & Comparison"
])

# === TAB 1 ===
with tab1:
    st.markdown("### 🎯 Track Analyzer")
    file = st.file_uploader("Upload a track (.mp3/.wav)", type=["mp3", "wav"])

    if file:
        path = f"app/audio/{file.name}"
        with open(path, "wb") as f:
            f.write(file.read())

        y, sr = librosa.load(path, sr=None)
        bpm, key = detect_bpm_key(y, sr)
        mood = analyze_mood(path)
        mood_color = get_mood_color(mood)

        def get_mood_icon(mood_text):
            mood_text = mood_text.lower()
            if "happy" in mood_text or "uplift" in mood_text: return "😊"
            if "calm" in mood_text or "chill" in mood_text: return "😌"
            if "dark" in mood_text or "emotional" in mood_text: return "😢"
            if "energetic" in mood_text or "hype" in mood_text: return "🔥"
            return "🎧"

        # === Display Track Metadata ===
        col1, col2 = st.columns(2)
        col1.metric("⏱️ BPM", bpm)
        col2.metric("🎼 Key", key)

        # === Mood Box ===
        mood_display = mood.strip()
        mood_icon = get_mood_icon(mood_display)
        color = get_mood_color(mood_display)  # Define the color variable

        st.markdown(f"""
            <div class="mood-box" style="--mood-color: {color}; --mood-color-glow: {color}44;">
                <h4>🧠 Mood</h4>
                <p>{mood_icon} {mood_display}</p>
            </div>
        """, unsafe_allow_html=True)

        # === Spacer Divider ===
        st.markdown("""
        <div style="margin-top: 25px; margin-bottom: 16px;">
            <hr style="border: none; height: 1px; background: linear-gradient(to right, #ff00ff33, #00ffff33);" />
        </div>
        """, unsafe_allow_html=True)

        # === Waveform Box ===
        st.markdown(f"""
        <div style="background-color: #1a1a1a; border: 1px solid #00ffff33;
                    border-radius: 12px; padding: 16px; margin-bottom: 16px;
                    box-shadow: 0 0 10px #00ffff22;">
            <h3 style='color: #00ffff;'>🎧 Audio Waveform (Emotion-Based)</h3>
            <p style='color: #cccccc; font-size: 14px;'>
                🎨 Emotion Color: <code style='color:{mood_color};'>{mood_color}</code>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # === Plot Waveform ===
        fig = generate_emotion_waveform(y, sr, mood=mood, track_name=file.name)
        st.pyplot(fig)

        # === Web Audio API EQ Visualizer ===
        with open(path, "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()

        eq_html = f"""
        <audio id="audio" controls style="width:100%; margin-bottom:1rem;">
            <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
        </audio>
        <div id="eq-bars" style="display: flex; align-items: flex-end; height: 120px;
             background: #111; padding: 10px; border-radius: 8px; gap: 3px;"></div>

        <script>
        const audio = document.getElementById("audio");
        const eq = document.getElementById("eq-bars");
        const numBars = 64;

        function getColor(i) {{
            const hue = {{"#FF00FF": 300, "#00FFFF": 180, "#00FF99": 160, "#00FF00": 120}}["{mood_color}"] || 270;
            return `hsl(${{hue + (i * 2)}}, 100%, 60%)`;
        }}

        for (let i = 0; i < numBars; i++) {{
            const bar = document.createElement("div");
            bar.style.flex = "1";
            bar.style.height = "10px";
            bar.style.borderRadius = "4px 4px 0 0";
            bar.style.background = getColor(i);
            bar.style.boxShadow = "0 0 6px white";
            bar.style.transition = "height 0.1s ease";
            eq.appendChild(bar);
        }}

        const bars = eq.children;
        const ctx = new AudioContext();
        const src = ctx.createMediaElementSource(audio);
        const analyser = ctx.createAnalyser();
        src.connect(analyser);
        analyser.connect(ctx.destination);
        analyser.fftSize = 128;
        const data = new Uint8Array(analyser.frequencyBinCount);

        function animate() {{
            requestAnimationFrame(animate);
            analyser.getByteFrequencyData(data);
            for (let i = 0; i < bars.length; i++) {{
                const val = data[i] / 255;
                bars[i].style.height = `${{Math.round(val * 100)}}px`;
            }}
        }}

        audio.onplay = () => {{
            if (ctx.state === 'suspended') ctx.resume();
            animate();
        }};
        </script>
        """

        components.html(eq_html, height=200)
# === TAB 2 ===
with tab2:
    st.markdown("### 🎚️ DJ Set Optimizer")
    files = st.file_uploader("Upload multiple files", type=["mp3", "wav"], accept_multiple_files=True)

    if files:
        tracks = []
        for f in files:
            path = f"app/audio/{f.name}"
            with open(path, "wb") as out:
                out.write(f.read())
            y, sr = librosa.load(path, sr=None)
            bpm, key = detect_bpm_key(y, sr)
            mood = analyze_mood(path)
            energy = calculate_energy_profile(y)
            tracks.append({"filename": f.name, "bpm": bpm, "key": key, "mood": mood, "energy": energy})

        tracks = sorted(tracks, key=lambda x: x["energy"])
        for t in tracks:
            t["role"] = classify_set_role(t["bpm"], t["energy"], t["mood"])

        st.markdown("### 🎬 Set Arc Builder")
        arc_display = " ➝ ".join([f"{t['role']} ({t['filename'].split('.')[0][:10]})" for t in tracks])
        st.markdown(f"<div style='padding:12px; background:#111; color:white; border-left:5px solid #FF00FF; border-radius:8px;'>🎛️ {arc_display}</div>", unsafe_allow_html=True)

        st.markdown("### 📊 Energy Curve")
        st.plotly_chart(generate_plotly_energy_curve(tracks), use_container_width=True)

        st.markdown("### 🔗 Transition Suggestions")
        for t in suggest_best_transitions(tracks):
            st.markdown(f"<div style='padding:10px; background:#111; margin:10px 0; border-left:4px solid #FF00FF;'><b>{t['from']} ➜ {t['to']}</b><br><small>{t['reason']}</small></div>", unsafe_allow_html=True)

        df = pd.DataFrame(tracks)[["filename", "bpm", "key", "mood", "energy"]]
        st.download_button("📥 Download CSV", df.to_csv(index=False).encode(), "dj_set.csv", "text/csv")


# === TAB 3: Performance Mode (Dual Deck) ===
with tab3:
    st.markdown("## 🎛️ DJ Performance Mode (Dual Deck)")
    deck_cols = st.columns(2)

    for i, col in enumerate(deck_cols):
        deck_id = f"Deck {i+1}"
        with col:
            st.markdown(f"### 🎵 {deck_id}")
            uploaded_file = st.file_uploader(f"Upload Track for {deck_id}", type=["mp3", "wav"], key=f"deck{i}")

            if uploaded_file:
                path = f"app/audio/{uploaded_file.name}"
                with open(path, "wb") as f:
                    f.write(uploaded_file.read())

                y, sr = librosa.load(path, sr=None)
                bpm, key = detect_bpm_key(y, sr)
                mood = analyze_mood(path)
                energy = calculate_energy_profile(y)
                role = classify_set_role(bpm, energy, mood)
                color = get_mood_color(mood)

                st.metric("⏱️ BPM", bpm)
                st.metric("🎼 Key", key)

                st.markdown(f"""
                <div style='padding:10px 15px; background:#1a1a1a;
                            border-left:6px solid {color}; border-radius:10px;
                            margin-top:15px; box-shadow:0 0 8px {color}44;'>
                    <h4 style='margin-bottom:8px; color:{color};'>🧠 Mood</h4>
                    <p style='margin:0; font-size:1.1rem; color:white;'>{mood}</p>
                </div>
                """, unsafe_allow_html=True)

                fig = generate_emotion_waveform(y, sr, mood=mood, track_name=uploaded_file.name)
                st.pyplot(fig)

                with open(path, "rb") as f:
                    audio_bytes = f.read()
                    audio_base64 = base64.b64encode(audio_bytes).decode()

                eq_html = f"""
                <audio id="audio{i}" controls style="width:100%; margin-bottom:1rem;">
                    <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                </audio>
                <div id="eq-bars{i}" style="display: flex; align-items: flex-end; height: 120px;
                    background: #111; padding: 10px; border-radius: 8px; gap: 3px;"></div>

                <script>
                const audio = document.getElementById("audio{i}");
                const eq = document.getElementById("eq-bars{i}");
                const numBars = 64;
                const moodColor = "{color}";
                function getColor(i) {{
                    const hue = {{"#FF00FF": 300, "#00FFFF": 180, "#00FF99": 160, "#00FF00": 120}}[moodColor] || 270;
                    return `hsl(${{hue + (i * 2)}}, 100%, 60%)`;
                }}
                for (let j = 0; j < numBars; j++) {{
                    const bar = document.createElement("div");
                    bar.style.flex = "1";
                    bar.style.height = "10px";
                    bar.style.borderRadius = "4px 4px 0 0";
                    bar.style.background = getColor(j);
                    bar.style.boxShadow = "0 0 6px white";
                    bar.style.transition = "height 0.1s ease";
                    eq.appendChild(bar);
                }}
                const bars = eq.children;
                const ctx = new AudioContext();
                const src = ctx.createMediaElementSource(audio);
                const analyser = ctx.createAnalyser();
                src.connect(analyser);
                analyser.connect(ctx.destination);
                analyser.fftSize = 128;
                const data = new Uint8Array(analyser.frequencyBinCount);
                function animate() {{
                    requestAnimationFrame(animate);
                    analyser.getByteFrequencyData(data);
                    for (let j = 0; j < bars.length; j++) {{
                        const val = data[j] / 255;
                        bars[j].style.height = `${{Math.round(val * 100)}}px`;
                    }}
                }}
                audio.onplay = () => {{
                    if (ctx.state === 'suspended') ctx.resume();
                    animate();
                }};
                </script>
                """
                components.html(eq_html, height=200)

    # 🎚️ Compare Deck A & B
    if all(f"deck{idx}" in st.session_state and st.session_state[f"deck{idx}"] for idx in range(2)):
        try:
            # Extract deck info
            deck_data = []
            for idx in range(2):
                file = st.session_state.get(f"deck{idx}")
                if file:
                    path = f"app/audio/{file.name}"
                    y, sr = librosa.load(path, sr=None)
                    bpm, key = detect_bpm_key(y, sr)
                    mood = analyze_mood(path)
                    energy = calculate_energy_profile(y)
                    role = classify_set_role(bpm, energy, mood)
                    color = get_mood_color(mood)
                    deck_data.append({
                        "name": file.name,
                        "bpm": bpm,
                        "key": key,
                        "mood": mood,
                        "energy": energy,
                        "role": role
                    })

            if len(deck_data) == 2:
                a, b = deck_data
                bpm_diff = abs(a["bpm"] - b["bpm"])
                key_match = "Yes" if a["key"] == b["key"] else "No"
                energy_trend = "⬆️ Increasing" if b["energy"] > a["energy"] else "⬇️ Decreasing"

                st.markdown("---")
                st.markdown("### 🎚️ Deck Comparison")
                st.markdown(f"""
                - **BPM Diff:** {bpm_diff:.1f}  
                - **Key Match:** {key_match}  
                - **Mood Shift:** {a["mood"]} → {b["mood"]}  
                - **Energy:** {a["energy"]:.2f} → {b["energy"]:.2f} {energy_trend}
                """)

                # === AI TIP from Cohere
                import cohere
                co = cohere.Client(st.secrets["COHERE_API_KEY"])
                transition_prompt = f"""
                You are a DJ assistant. Suggest a creative 1-line tip to transition from:
                Deck A: "{a['name']}" (BPM: {a['bpm']}, Key: {a['key']}, Mood: {a['mood']}, Energy: {a['energy']:.2f}, Role: {a['role']})
                into
                Deck B: "{b['name']}" (BPM: {b['bpm']}, Key: {b['key']}, Mood: {b['mood']}, Energy: {b['energy']:.2f}, Role: {b['role']})
                Tip:
                """
                response = co.generate(model="command-light", prompt=transition_prompt.strip(), max_tokens=50)
                tip = response.generations[0].text.strip()

                st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style='margin-top:20px; padding:16px; background:#111;
                            border-left:5px solid #00FFFF; border-radius:8px;
                            box-shadow: 0 0 8px #00FFFF44;'>
                    <b style='color:#00FFFF;'>💡 AI Transition Tip:</b><br>
                    <span style='color:white;'>{tip}</span>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            st.warning("⚠️ Could not generate AI transition tip. Error: " + str(e))


# === TAB 4: 📚 Library Insight ===
with tab4:
    st.markdown("### 📚 Library Insight (Bulk Track Analyzer)")
    files = st.file_uploader("Upload multiple tracks (.mp3/.wav)", type=["mp3", "wav"], accept_multiple_files=True)

    if files:
        st.info(f"🔍 Analyzing {len(files)} tracks...")

        all_tracks = []
        for f in files:
            temp_path = f"app/audio/{f.name}"
            with open(temp_path, "wb") as out:
                out.write(f.read())

            try:
                y, sr = librosa.load(temp_path, sr=None)
                bpm, key = detect_bpm_key(y, sr)
                mood = analyze_mood(temp_path)
                energy = calculate_energy_profile(y)
                all_tracks.append({
                    "Track": f.name,
                    "BPM": bpm,
                    "Key": key,
                    "Mood": mood,
                    "Energy": round(energy, 3)
                })
            except Exception as e:
                all_tracks.append({
                    "Track": f.name,
                    "BPM": "❌",
                    "Key": "❌",
                    "Mood": f"Error: {e}",
                    "Energy": "❌"
                })

        df = pd.DataFrame(all_tracks)
        st.dataframe(df, use_container_width=True)

        st.download_button("📥 Download CSV", df.to_csv(index=False).encode(), "library_analysis.csv", "text/csv")

        st.success("✅ All tracks analyzed. You can now sort, download, or use this data for set prep.")

import streamlit as st
from utils import (
    get_spotify_token,
    search_spotify_tracks,
    get_spotify_audio_features,
    search_youtube_videos
)

YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
SPOTIFY_CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]

# === TAB 5: Discovery & Comparison (Spotify Client Token - No Login) ===
import requests
import base64

# 🔐 Get Spotify Access Token using Client Credentials Flow
def get_spotify_token():
    client_id = st.secrets["SPOTIPY_CLIENT_ID"]
    client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
    token_url = "https://accounts.spotify.com/api/token"
    encoded = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    res = requests.post(token_url, headers=headers, data=data)
    res.raise_for_status()
    return res.json()["access_token"]

# 🔍 Search Spotify
@st.cache_data(show_spinner=False, ttl=3600)
def search_spotify_tracks(query, token, limit=5):
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()["tracks"]["items"]

# 📈 Fetch Audio Features (BPM, energy, key, etc.)
def get_spotify_features(track_id, token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

# === TAB 5 UI ===
with tab5:
    st.markdown("### 🔍 Discover & Analyze via Spotify (No Login)")
    query = st.text_input("Search any track, artist, or mood")
    if query:
        try:
            token = get_spotify_token()
            results = search_spotify_tracks(query, token)

            for track in results:
                name = track["name"]
                artist = ", ".join([a["name"] for a in track["artists"]])
                preview_url = track["preview_url"]
                album_img = track["album"]["images"][0]["url"]
                track_id = track["id"]

                st.image(album_img, width=160)
                st.markdown(f"**{name}** by *{artist}*")

                if preview_url:
                    st.audio(preview_url)

                    try:
                        features = get_spotify_features(track_id, token)
                        bpm = round(features["tempo"])
                        key_index = features["key"] % 12
                        key_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
                        key = key_names[key_index]
                        energy = round(features["energy"] * 100, 1)
                        danceability = round(features["danceability"] * 100, 1)

                        # Simulated mood
                        if energy > 75:
                            mood = "Hype"
                        elif energy > 55:
                            mood = "Energetic"
                        elif energy > 35:
                            mood = "Mellow"
                        else:
                            mood = "Chill"

                        st.markdown(f"BPM: **{bpm}** | Key: **{key}** | Energy: **{energy}%** | Mood: **{mood}**")
                    except Exception as e:
                        st.warning(f"⚠️ Feature data unavailable: {e}")
                else:
                    st.warning("⚠️ No preview available for this track")

        except Exception as e:
            st.error(f"❌ Spotify error: {e}")
