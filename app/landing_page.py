# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence

import os
import streamlit as st
from PIL import Image

st.set_page_config(page_title="MoodMixr | AI-Powered DJ Intelligence", layout="wide")

# ------------------------- CSS Styling -------------------------
st.markdown(
    """
<style>
.big-title {
    font-size: 3em; font-weight: bold; text-align: center; color: #ffffff; padding-top: 1rem;
}
.sub-title {
    font-size: 1.2em; text-align: center; color: #bbbbbb;
}
.section-header {
    font-size: 1.8em; margin-top: 2rem; margin-bottom: 1rem; color: #eeeeee;
}
.feature-box {
    background-color: #111111; padding: 1.2rem; border-radius: 10px; margin-bottom: 1.5rem; color: #eeeeee;
}
footer {
    text-align: center; font-size: 0.8rem; padding: 2rem; color: #888888;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------- Branding -------------------------
st.markdown('<div class="big-title">MoodMixr</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Human Creativity meets Intelligent Audio Agents — built for the next generation of DJs.</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ------------------------- Vision -------------------------
st.markdown(
    '<div class="section-header">What is MoodMixr?</div>', unsafe_allow_html=True
)
st.markdown(
    """
MoodMixr is a modular AI-powered ecosystem designed to help DJs and producers create unforgettable sets with clarity, confidence, and emotion.  
Each audio agent performs a specific task — from mood detection to BPM, key, transition roles, energy flow, and vocal presence — running locally in Dockerized containers.  
The platform supports professional audio formats (FLAC, WAV, MP3), ensuring true fidelity and privacy-first execution.

You upload.  
Agents analyze.  
You build the future of sound.
"""
)

# ------------------------- Features -------------------------
st.markdown('<div class="section-header">Key Features</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """<div class="feature-box">
🧠 AI Intelligence Stack<br>
- Mood Detection (emotional profile)<br>
- Audio Analysis (BPM, Key, Energy, Silence)<br>
- Agent-Based Architecture (Docker + FastAPI)<br>
- Local Execution (No cloud dependency)<br>
</div>""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """<div class="feature-box">
🎧 Pro DJ Tools<br>
- Upload FLAC/WAV/MP3 with waveform visuals<br>
- Spotify + YouTube fallback support<br>
- JSON/Crate export for Serato/Rekordbox<br>
- Set optimization with transition suggestions<br>
</div>""",
        unsafe_allow_html=True,
    )

# ------------------------- Screenshots -------------------------
st.markdown(
    '<div class="section-header"> Product Preview</div>', unsafe_allow_html=True
)

screenshot_folder = "A:/MoodMixr/screenshots"  # Windows-style absolute path

if os.path.exists(screenshot_folder):
    screenshots = sorted(
        [
            os.path.join(screenshot_folder, f)
            for f in os.listdir(screenshot_folder)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
    )
    if screenshots:
        for img_path in screenshots:
            st.image(Image.open(img_path), use_container_width=True)
    else:
        st.warning("No screenshots found in the screenshots folder.")
else:
    st.error("Screenshot folder not found at A:/MoodMixr/screenshots.")

# ------------------------- Waitlist -------------------------
st.markdown(
    '<div class="section-header"> Join the Waitlist</div>', unsafe_allow_html=True
)
email = st.text_input("Enter your email to get early access + updates:")
if st.button("Join Waitlist"):
    if email:
        st.success(
            f"Thanks! You’ve been added: {email} (This is currently a placeholder. No backend yet.)"
        )
    else:
        st.warning("Please enter a valid email.")

# ------------------------- Hindu Blessing -------------------------
st.markdown("---")
st.markdown(
    """
<center>
🙏 *May Lord Shiva protect our path, Maa Saraswati guide our code, and Krishna inspire the rhythm within.*
</center>
""",
    unsafe_allow_html=True,
)

# ------------------------- Next Steps -------------------------
st.markdown('<div class="section-header">Next Steps</div>', unsafe_allow_html=True)
st.markdown(
    """
- Add Genre Detection Agent (audio-based and model-based)
- Orchestrate agent workflows via n8n
- Build Export Agent for Rekordbox & Serato crates
- Build the VST plugin bridge for DAWs
- Launch Public Beta Landing Page with shareable insights
- Continue to share our progress on LinkedIn, Product Hunt, and Reddit
"""
)

# ------------------------- Footer -------------------------
st.markdown("---")
st.markdown(
    """
<footer>
MoodMixr v0.95 | Built by Karmonic (Akshay Surti)<br>
© 2025. Sacred Sound. Infinite Vibe. All Rights Reserved.
</footer>
""",
    unsafe_allow_html=True,
)
