
---

### ✅ `project.md` (Internal Dev Roadmap)

```md
# 📁 MoodMixr Development Log

## 🔖 v0.3 – Agent Architecture + Vocal Detection (Released)

- Added modular agent system
- Integrated VocalDetectorAgent with confidence score
- Created SetOptimizerAgent for opener → peak → closer classification
- Updated summary, UI, and JSON exports
- Laid the groundwork for crate upload + mix optimization

---

## 🔜 v0.4 – Multi-Track Mode + Set Flow Visualizer

### 🎯 Goals:
- [ ] Add multi-file upload crate UI
- [ ] Integrate `SetOptimizerAgent.sort_tracks()` across full crate
- [ ] Visualize set flow (timeline or radar)
- [ ] Plot energy vs. time (curve)
- [ ] Display full setlist as “export-ready” crate
- [ ] Add smart `TransitionRecommenderAgent` logic
- [ ] Optional: draggable track order editor

---

## 🧠 v0.5 (Future Ideas)

- ML-powered vocal detection (Demucs/Spleeter)
- Genre classifier (using cohere or open-source models)
- Mix preview tool (simulate real-time transitions)
- EQ visualizer (low/mid/high color bands)
- Save sets to database or cloud
