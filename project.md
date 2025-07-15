# 🎧 MoodMixr Project Tracker

AI-powered DJ Insight Tool for Pros  
Built with: Python, Streamlit, Librosa, Cohere

---

## ✅ COMPLETED FEATURES

- 🎵 Single Track Analyzer
  - [x] Upload MP3/WAV
  - [x] BPM + Key Detection
  - [x] Mood Detection via Cohere
  - [x] Emotion-based waveform plot
  - [x] Multi-color EQ bar animation (simulated)
  - [x] Mood summary with emoji
  - [x] Track player with waveform and visualizer

- 🚀 DJ Set Optimizer
  - [x] Upload multiple tracks
  - [x] Auto-detect BPM, Key, Mood, Energy
  - [x] AI role classifier (Opener / Peak / Closer)
  - [x] Energy Curve Visualization (Plotly)
  - [x] Best transition suggestions
  - [x] DJ Set Arc Builder (flow path)
  - [x] CSV export of analyzed set

---

## 🔁 IN PROGRESS

- 🎛️ Real-Time Animated EQ (with FFT loop)
  - [x] Static FFT
  - [x] Animated simulation using st.empty() ✅
  - [ ] Next: Fully synced to audio (Web Audio API)

---

## 🛠 PLANNED FEATURES

- 🎚️ Set Arc Drag-and-Drop Editor
- 💿 Track Segment Analyzer (Intro / Drop / Outro)
- 🧠 Mood Use Case Generator (e.g., "Use during sunset sets")
- 🎥 Performance Mode View (Fullscreen player, EQ, and waveform)
- 📂 GitHub Repo with Live App + Setup Instructions
- 📦 Streamlit Cloud Deployment or Hugging Face Space
- 🎨 Mood-Based UI Theme Switcher (dark/light + mood color glow)

---

## 📌 NEXT PRIORITY
> 🎛️ Build Real-Time EQ synced to playback (Web Audio API inside components.html)

---

## 📁 Project Structure
MoodMixr/
├── app/
│ └── moodmixr_app.py
│ └── utils.py
│ └── audio/
├── .streamlit/
│ └── secrets.toml
├── project.md ✅ <— this file
├── requirements.txt
├── README.md



---

> Maintained by: [Akshay Surti a.k.a Karmonic + MoodMixr + GPT 💜]
