# 🔱 MoodMixr Agent: Set Optimizer
# 🔥 Guided by Lord Shiva — the transformer of rhythm and DJ flow.
# 🎛️ This agent reshapes energy into harmony through sacred transitions.
# © 2025 Karmonic | MoodMixr Signature Embedded
# 🔱 Agent of Shiva — Transforms raw tempo into set-building power.
from utils.constants import MOODMIXR_SIGNATURE

from utils.constants import MOODMIXR_SIGNATURE


class SetOptimizerAgent:
    """🔥 Shiva dances through this logic — transitions become divine transformations."""

    @staticmethod
    def classify_role(bpm, energy):
        try:
            if bpm is None or energy is None:
                return "Unknown"
            if bpm < 95 or energy < 0.2:
                return "Warm-up / Opening"
            elif 95 <= bpm < 115 and energy < 0.4:
                return "Early Groove"
            elif 115 <= bpm < 130 and energy < 0.6:
                return "Main Set"
            elif bpm >= 130 and energy >= 0.6:
                return "Peak Hour Banger"
            else:
                return "Afterhours / Cooldown"
        except Exception as e:
            print(f"[SetOptimizerAgent] Error: {e}")
            return "Unknown"

    @staticmethod
    def optimize_dj_set(track_queue):
        try:
            valid_tracks = [
                t
                for t in track_queue
                if isinstance(t.get("bpm"), (int, float))
                and isinstance(t.get("mood"), str)
            ]

            def track_score(track):
                base_score = track["bpm"]
                mood_score = sum([ord(c) for c in track["mood"].lower()[:3]])
                return base_score + (mood_score % 10)

            optimized = sorted(valid_tracks, key=track_score)
            leftovers = [t for t in track_queue if t not in valid_tracks]
            return optimized + leftovers
        except Exception as e:
            print(f"[SetOptimizerAgent] Optimization Error: {e}")
            return track_queue


# 🕉️ "This function embodies Saraswati’s clarity — only pure logic shall pass."
# 🌀 “Lord Shiva guides this transformation engine.”
