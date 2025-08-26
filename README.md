# MoodMixr

**MoodMixr** is an AI-powered DJ Insight Engine that helps DJs, producers, and playlist curators make smarter decisions with their music sets. Built with modular AI agents, it analyzes track audio, emotion, structure, and energy — and turns raw audio into set-ready insights.

> Think of it as your DJ Copilot — combining signal processing + large language models for live or studio workflows.

---

## Features

- **VocalDetectorAgent**  
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
<img width="2560" height="2320" alt="MoodMixr-07-29-2025_12_12_PM" src="https://github.com/user-attachments/assets/25358d21-2379-4670-97a1-e1310ead4336" />
<img width="1243" height="1911" alt="MoodMixr-07-31-2025_02_17_PM" src="https://github.com/user-attachments/assets/34440ea8-e9d3-478f-b4b7-d3a693a056ab" />
<img width="2560" height="6134" alt="MoodMixr-07-30-2025_02_41_PM" src="https://github.com/user-attachments/assets/4fe2c748-2d7b-404f-9987-36caaedc228b" />
<img width="1278" height="2329" alt="MoodMixr-07-30-2025_03_06_PM" src="https://github.com/user-attachments/assets/2be7233b-f90c-4060-a558-b298c36b4db0" />





---

## How to Run Locally

```bash
git clone https://github.com/karmonic540/MoodMixr.git
cd MoodMixr
pip install -r requirements.txt
streamlit run app/moodmixr_app.py
