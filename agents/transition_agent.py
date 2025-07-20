class TransitionRecommenderAgent:

    @staticmethod
    def recommend(track_path, bpm, key, mood, energy):
        try:
            transitions = []

            # Rule-based + mood logic
            if energy >= 0.05:
                transitions.append("Follow up with a high-energy track")
            else:
                transitions.append("Use a chilled track or breakdown moment")

            # BPM-based
            if bpm < 85:
                transitions.append("Mix into a slow trap or downtempo groove")
            elif 85 <= bpm < 110:
                transitions.append("Transition to mid-tempo hip-hop or funk")
            elif 110 <= bpm < 128:
                transitions.append("Groove into tech house or indie dance")
            else:
                transitions.append("Peak hour track — move into big room EDM or hard techno")

            # Mood overlay
            transitions.append(f"Mood: {mood} — consider setting up a {mood.lower()} vibe next")

            return transitions

        except Exception as e:
            print(f"[TransitionRecommenderAgent] Error: {e}")
            return ["Could not generate suggestions."]
