# === moodmixr_app.py (Updated with Real-Time EQ + Set Arc Builder) ===
import streamlit as st
import os
import time
import librosa
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import matplotlib.pyplot as plt


def plot_animated_eq(y, mood, sr):
    from scipy.fft import fft
    from matplotlib.cm import get_cmap

    container = st.empty()
    cmap = get_cmap("plasma")
    chunk_size = 2048

    for i in range(10):  # 10 frames ~ 5 seconds
        start = i * chunk_size
        end = start + chunk_size
        if end > len(y):
            break

        y_chunk = y[start:end]
        yf = np.abs(fft(y_chunk))[:chunk_size // 2]
        if np.max(yf) == 0:
            continue
        yf = yf / np.max(yf)

        bar_colors = [cmap(i / len(yf)) for i in range(len(yf))]

        fig, ax = plt.subplots(figsize=(10, 2), facecolor="#0D0D0D")
        ax.set_facecolor("#0D0D0D")
        ax.bar(np.arange(len(yf)), yf, color=bar_colors, width=2.0)
        ax.set_ylim(0, 1)
        ax.axis("off")
        container.pyplot(fig)
        time.sleep(0.5)

from streamlit.components.v1 import html
from scipy.fft import fft
from utils import (
    detect_bpm_key,
    analyze_mood,
    calculate_energy_profile,
    generate_emotion_waveform,
    generate_plotly_energy_curve,
    get_bpm_animation_speed,
    get_mood_color,
    suggest_best_transitions,
    classify_set_role
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

tab1, tab2, tab3 = st.tabs(["🎯 Track Analyzer", "🎚️ DJ Set Optimizer", "🎛️ Performance Mode"])


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

        def get_mood_icon(mood_text):
            mood_text = mood_text.lower()
            if "happy" in mood_text or "uplift" in mood_text: return "😊"
            if "calm" in mood_text or "chill" in mood_text: return "😌"
            if "dark" in mood_text or "emotional" in mood_text: return "😢"
            if "energetic" in mood_text or "hype" in mood_text: return "🔥"
            return "🎧"

        # 🎚️ Display BPM, Key
        col1, col2 = st.columns(2)
        col1.metric("⏱️ BPM", bpm)
        col2.metric("🎼 Key", key)

        # 🧠 Mood Summary
        mood_display = mood.strip()
        mood_icon = get_mood_icon(mood_display)
        st.markdown(f"""
        <div style='padding:15px 20px; background:#1a1a1a;
                    border-left:6px solid #FF00FF; border-radius:10px;
                    margin-top:25px; box-shadow:0 0 8px #ff00ff44;'>
            <h4 style='margin-bottom:8px; color:#FF00FF;'>🧠 Mood</h4>
            <p style='margin:0; font-size:1.1rem; color:white;'>{mood_icon} {mood_display}</p>
        </div>
        """, unsafe_allow_html=True)

        # 📈 Waveform
        fig = generate_emotion_waveform(y, sr, mood=mood, track_name=file.name)
        st.pyplot(fig)

        # 🔊 Web Audio API EQ (Live Playback)
        from streamlit.components.v1 import html
        import base64

        with open(path, "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()

        eq_color = get_mood_color(mood) if 'mood' in locals() else "#FF00FF"

        eq_html = f"""
        <audio id=\"audio\" controls style=\"width:100%; margin-bottom:1rem;\">
          <source src=\"data:audio/wav;base64,{audio_base64}\" type=\"audio/wav\">
        </audio>
        <div id=\"eq-bars\" style=\"display: flex; align-items: flex-end; height: 120px;
             background: #111; padding: 10px; border-radius: 8px; gap: 3px;\"></div>

        <script>
        const audio = document.getElementById("audio");
        const eq = document.getElementById("eq-bars");
        const numBars = 64;

        function getColor(i) {{
          const hue = {{"#FF00FF": 300, "#00FFFF": 180, "#00FF99": 160, "#00FF00": 120}}["{eq_color}"] || 270;
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

        html(eq_html, height=200)




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

# === TAB 3: Performance Mode ===
with tab3:
    st.markdown("## 🎛️ DJ Performance Mode")
    perf_files = st.file_uploader("🎵 Upload Your Set (multiple tracks)", type=["mp3", "wav"], accept_multiple_files=True, key="perfmode")

    if perf_files:
        track_names = [f.name for f in perf_files]
        selected = st.selectbox("🎧 Select a Track to Perform", track_names)
        selected_file = next(f for f in perf_files if f.name == selected)

        path = f"app/audio/{selected_file.name}"
        with open(path, "wb") as f:
            f.write(selected_file.read())

        y, sr = librosa.load(path, sr=None)
        bpm, key = detect_bpm_key(y, sr)
        mood = analyze_mood(path)
        energy = calculate_energy_profile(y)
        role = classify_set_role(bpm, energy, mood)
        color = get_mood_color(mood)

        st.markdown(f"<h2 style='text-align:center; color:{color};'>🎧 Now Playing: <br><span style='font-size:28px;'>{selected_file.name}</span></h2>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric("⏱️ BPM", bpm)
        col2.metric("🎼 Key", key)
        col3.markdown(f"<h4 style='margin-top:20px;'>🔥 Role: <span style='color:{color};'>{role}</span></h4>", unsafe_allow_html=True)

        fig = generate_emotion_waveform(y, sr, mood=mood, track_name=selected_file.name)
        st.pyplot(fig)

        # === Web Audio API EQ
        import base64
        with open(path, "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode()

        eq_html = f"""
        <audio id="audio" controls style="width:100%; margin-bottom:1rem;">
          <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
        </audio>
        <div id="eq-bars" style="display: flex; align-items: flex-end; height: 130px;
             background: #000; padding: 12px; border-radius: 10px; gap: 4px;"></div>

        <script>
        const audio = document.getElementById("audio");
        const eq = document.getElementById("eq-bars");
        const numBars = 80;

        function getColor(i) {{
          const hue = {{"#FF00FF": 300, "#00FFFF": 180, "#00FF99": 160, "#00FF00": 120}}["{color}"] || 280;
          return `hsl(${{hue + i * 2}}, 100%, 60%)`;
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
        analyser.fftSize = 256;
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
        html(eq_html, height=220)

        # === AI SET TIP
        try:
            import cohere
            co = cohere.Client(st.secrets["COHERE_API_KEY"])
            track_info = f"{selected_file.name} | BPM: {bpm} | Key: {key} | Mood: {mood} | Role: {role} | Energy: {energy:.2f}"
            prompt = f"You are a DJ set assistant. Give a 1-line set tip for the track below.\nTrack: {track_info}\nTip:"
            response = co.generate(model="command-light", prompt=prompt, max_tokens=50)
            set_tip = response.generations[0].text.strip()

            st.markdown(f"<div style='padding:15px; margin-top:25px; background:#111; border-left:5px solid {color}; border-radius:8px;'>"
                        f"<b style='color:{color};'>💡 Set Tip:</b><br><span style='color:white;'>{set_tip}</span></div>", unsafe_allow_html=True)
        except Exception as e:
            st.warning("No AI tip generated. Check API.")


