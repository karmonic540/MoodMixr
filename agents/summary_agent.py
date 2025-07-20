class SummaryAgent:

    @staticmethod
    def generate_summary(filename, bpm, key, mood, set_role, has_vocals):
        mood_clean = mood.title()
        vocal_text = "Vocals" if has_vocals else "No Vocals"
        return f"{filename} | {bpm} BPM | {key} | {mood_clean} | {set_role} | {vocal_text}"