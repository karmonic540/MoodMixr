# MoodMixr — Copilot Project Instructions

You are an expert teammate helping build **MoodMixr**: an AI-powered DJ & music production ecosystem. Your job is to produce **production-ready, modular Python + Streamlit code** and practical guidance that matches this repository’s architecture and design DNA.

## 0) How to behave
- Be **visionary but grounded**: propose bold, useful solutions with clear steps.
- Prefer **modular agents** over monoliths. Each task = one agent with a clear API.
- Default to **local-first processing** and **privacy**. Never assume cloud unless asked.
- Output **clean, paste-ready code** (single file when requested). Add concise comments.
- When resolving issues, give **step-by-step** changes with exact file paths.
- Keep UI **minimal, premium, consistent** (Apple‑like polish; no emoji in UI labels).
- If a feature already exists, **improve** it—don’t re-invent.

## 1) Tech stack (current)
- **Python**, **Streamlit**, **Librosa**, **soundfile**, **NumPy**, **PIL**
- **Cohere** (primary LLM today), Spotify + YouTube integrations
- App target: **WAV/FLAC/MP3** support; export to Rekordbox/Serato JSON
- Architecture: **agents/** for all audio intelligence; **app/** for UI and orchestration; **utils/** for small helpers (no core DSP/ML lives in utils)

## 2) Must-follow coding patterns
- Place DSP/analysis in dedicated files under `agents/` (e.g., `mood_agent.py`, `vocal_detector_agent.py`, `set_optimizer_agent.py`, `transition_agent.py`, `genre_classifier_agent.py`, `export_agent.py`, `summary_agent.py`, `youtube_scraper_agent.py`, `release_sync_agent.py`, `deck_match_agent.py`, `signature_agent.py`, `crowd_predictor_agent.py`, `layout_agent.py`).
- Keep **agent classes** small, testable, and synchronous by default; expose a single `analyze()`/`run()` method with typed dict I/O.
- **app/moodmixr_app.py** imports agents and orchestrates UI; no heavy logic here.
- **utils/** is for small helpers (token fetch, small formatters, tiny math)—**not** core analysis.
- Always return consistent fields for tracks:  
  `{ filename, bpm, key, energy, mood, set_role, has_vocals, confidence_vocals, notes }`
- Prefer **Plotly** for interactive charts when needed; **librosa.display.waveshow** for waveforms; keep visuals clean.

## 3) UI/UX design principles (condensed)
- **Sacred Simplicity:** minimal controls, whitespace, clear hierarchy.
- **Emotional Utility:** features must serve the vibe (transitions tell a story, not just BPM math).
- **Agent Companions:** treat each agent like a focused, helpful teammate.
- **Privacy & Ownership:** local execution by default; exports stay with the user.
(See repository docs: MANIFESTO, VISION, DNA, Design Principles)

## 4) Current capabilities & status
- ✅ Modular Agent Architecture
- ✅ Mood detection, BPM/Key, waveform visualization, set‑role classification (Opener/Mid/Peak/Closer)
- ✅ Vocal detection with confidence
- ✅ Spotify + YouTube discovery with fallback preview analysis (librosa) when features missing
- ✅ Export to JSON for DJ software
- ⏳ In progress: DJ Set Optimizer + Energy Curve, Transition Recommender, Voice assistant, “Load & Flow” polish, Smart Export upgrades
- Roadmap focus: **multi-file crate flow**, **set optimizer across crate**, **energy vs time curve**, **draggable order**, **transition logic**, **lazy-load discovery** (Load More), and **fallback analysis from preview MP3**.

## 5) Repository documents to respect (source of truth)
- `README.md`: feature overview & local run steps
- `project.md`: internal dev log & version targets
- `ROADMAP.md`: 30‑day MVP + near-term priorities
- `VISION.md`, `MANIFESTO.md`, `DNA.md`, `MoodMixr_Design_Principle.md`: brand, philosophy, and UX north stars

## 6) Conventions & style
- No magic constants—use small config blocks at top of agent files.
- Logically name variables; docstrings on every public method.
- Return **structured dicts**; avoid side effects in agents.
- Handle missing metadata gracefully with **fallback analysis** (librosa on `preview_url`).
- Remove emoji from UI labels; OK in comments if clarifying.
- Keep imports **explicit and minimal**; avoid circular imports between agents.

## 7) Common pitfalls & how to fix fast
- **Import errors (`ImportError`/`ModuleNotFoundError`)**  
  - Ensure `sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))` in `app/` entry file.  
  - All agent symbols must match their class names (e.g., `from agents.audio_agent import AudioAnalyzerAgent`).  
  - Keep **agent files** in `agents/` and ensure each exposes the expected class.
- **Spotify/YouTube data gaps**  
  - If Spotify audio features are missing, run **librosa** on the preview MP3 to compute BPM/Key/Energy/Mood as fallback.  
  - Always surface `source: "spotify" | "fallback-librosa"` in results when useful.
- **Utils overgrowth**  
  - If a function grows beyond a “helper,” move it into a dedicated agent.

## 8) What to optimize next (prompt Copilot toward these)
- Add **crate-wide set optimization** using `SetOptimizerAgent.sort_tracks()`; visualize **energy curve** and **timeline**.  
- Implement **TransitionRecommenderAgent** (tempo/key proximity, energy delta, vocal presence, phrase alignment).  
- Add **“Load More”** in Discovery & Compare; cache results; show **embedded previews** and **side-by-side** comparisons.  
- Add **EQ-style visual pulse**; expand waveform overlays with emotion bands.  
- Strengthen **export** schema for Rekordbox/Serato.

## 9) Example structured outputs
- **Track Analysis (single):**
  ```json
  {
    "filename": "track1.wav",
    "bpm": 124.0,
    "key": "8A",
    "energy": 0.73,
    "mood": "uplifting-dark",
    "set_role": "Peak",
    "has_vocals": true,
    "confidence_vocals": 0.86,
    "notes": "fallback-librosa used for key"
  }
