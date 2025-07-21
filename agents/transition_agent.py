# 🔄 MoodMixr Agent: Transition Recommender
# 🔱 Guided by Lord Shiva — the cosmic transformer of rhythm, flow, and intention.
# 🎧 Suggests divine transitions between tracks based on BPM, energy, and emotional mood.
# © 2025 Karmonic | MoodMixr Signature Embedded

class TransitionRecommenderAgent:
    """
    🔁 Shiva blesses this rhythm path — may transitions flow like sacred movement.
    """

    @staticmethod
    def recommend(track_path, bpm, key, mood, energy):
        try:
            transitions = []

            # 🔊 Energy logic
            if energy >= 0.7:
                transitions.append("🔥 Follow with a high-energy peak track")
            elif 0.4 <= energy < 0.7:
                transitions.append("🎯 Maintain energy with similar vibe or tension builder")
            else:
                transitions.append("🌙 Cooldown moment — use breakdown, ambient pad, or vocal cut")

            # 🎚️ BPM logic
            if bpm < 85:
                transitions.append("🌀 Mix into slow trap, ambient house, or chillhop")
            elif 85 <= bpm < 110:
                transitions.append("💫 Transition into mid-tempo hip-hop, funk, or Afrobeat")
            elif 110 <= bpm < 128:
                transitions.append("🔊 Groove into deep house, tech house, or melodic techno")
            else:
                transitions.append("🚀 Push into big room EDM, trance, or hard techno")

            # 🎭 Mood-based vibe extension
            vibe_map = {
                "Calm": "Float into dreamy or melodic textures",
                "Happy": "Uplift the crowd with joyful bounce",
                "Dark": "Descend into deeper hypnotic layers",
                "Energetic": "Explode into high-BPM burners or percussive tribal rhythms",
                "Sad": "Shift into emotional storytelling with vocals or strings",
                "Romantic": "Blend into vocal house or slow-burning deep grooves"
            }

            mood = mood.strip().capitalize()
            if mood in vibe_map:
                transitions.append(f"🧠 Mood cue: {vibe_map[mood]}")
            else:
                transitions.append(f"🔍 Explore a {mood.lower()}-inspired transition layer")

            # 🎼 Final tip
            transitions.append(f"🎼 Key: {key} — consider harmonic mixing or a 1-semitone jump for tension")

            return transitions

        except Exception as e:
            print(f"[TransitionRecommenderAgent] ❌ ERROR: {e}")
            return ["⚠️ Could not generate transition recommendations."]
