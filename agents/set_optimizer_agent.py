class SetOptimizerAgent:

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
