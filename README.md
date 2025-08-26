# MoodMixr

**MoodMixr** is an AI-powered DJ Insight Engine that helps DJs, producers, and playlist curators make smarter decisions with their music sets. Built with modular AI agents, it analyzes track audio, emotion, structure, and energy — and turns raw audio into set-ready insights.

> Think of it as your DJ Copilot — combining signal processing + large language models for live or studio workflows.

---

## Features

- 🎙**VocalDetectorAgent**  
  Detects vocals using audio signal features (mel spectrogram, HPR, ZCR, flatness), returns `Yes/No` + confidence %

- **SetOptimizerAgent**  
  Classifies tracks into: Opener, Mid-Set, Peak, Closer  
  (based on BPM + Energy + Mood)

- **SummaryAgent**  
  Generates a readable summary string (BPM, Key, Mood, Role, Vocals)

- **TransitionRecommenderAgent** *(coming soon)*  
  Suggests the best mix transitions between tracks in a set

- **ExportAgent**  
  Exports analysis as `.json` for integration into Rekordbox, Serato, etc.

- Modular Agent Architecture  
  Easy to plug in new agents for mood, genre, lyrics, ML models, etc.

---

## How It Works

1. Upload 1 or more tracks (WAV, MP3, FLAC)
2. App analyzes each file using the agents
3. Output includes:
   - BPM, Key, Energy
   - Mood + Set Role
   - Vocal Detection (+ confidence)
   - Suggested Transitions
4. Export to `.json` or view inside app

---

## Screenshots
<img width="1250" height="402" alt="image" src="https://github.com/user-attachments/assets/04b5f8e0-1698-4c82-8a31-09badc686c70" />
<img width="1241" height="1103" alt="image" src="https://github.com/user-attachments/assets/2a0b9571-dfe6-4c54-ae26-676de07365f7" />
<img width="811" height="550" alt="image" src="https://github.com/user-attachments/assets/74364933-e4bf-4671-bdd0-c17f569d72fc" />
<img width="820" height="1028" alt="image" src="https://github.com/user-attachments/assets/9c1e848e-96cc-414b-b2cd-7efcba9d2606" />



---

## How to Run Locally

```bash
git clone https://github.com/karmonic540/MoodMixr.git
cd MoodMixr
pip install -r requirements.txt
streamlit run app/moodmixr_app.py
