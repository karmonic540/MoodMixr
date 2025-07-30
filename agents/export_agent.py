# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
# Created: 2025-07-05 | Version: 0.9.0 | License: MIT + Karma Clause

import json
import os


class ExportAgent:
    @staticmethod
    def export_metadata(track_path, bpm, key, mood, energy, transitions):
        try:
            base_name = os.path.basename(track_path)
            export_name = os.path.splitext(base_name)[0] + "_analysis.json"
            export_path = os.path.join("data", "exports")

            if not os.path.exists(export_path):
                os.makedirs(export_path)

            metadata = {
                "filename": str(base_name),
                "BPM": int(bpm) if bpm is not None else None,
                "Key": str(key) if key is not None else "Unknown",
                "Mood": str(mood) if mood is not None else "Unknown",
                "Energy": float(energy) if energy is not None else 0.0,
                "TransitionSuggestions": [str(s) for s in transitions]
                if transitions
                else [],
            }

            full_path = os.path.join(export_path, export_name)
            with open(full_path, "w") as f:
                json.dump(metadata, f, indent=4)

            print(f"[ExportAgent] Exported to: {full_path}")

        except Exception as e:
            print(f"[ExportAgent] Error exporting metadata: {e}")
