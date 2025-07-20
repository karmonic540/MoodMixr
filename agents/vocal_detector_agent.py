import librosa
import numpy as np

class VocalDetectorAgent:

    @staticmethod
    def detect(track_path):
        print(f"[VDE] 🔍 Analyzing vocals for: {track_path}")
        try:
            y, sr = librosa.load(track_path, sr=None)

            # === 1. Mel Band Energy ===
            S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmin=300, fmax=3000)
            db = librosa.power_to_db(S, ref=np.max)
            mean_db = np.mean(db)
            std_db = np.std(db)

            # === 2. HPR (vocal has more harmonic energy than percussive)
            harmonic, percussive = librosa.effects.hpss(y)
            hpr = np.mean(np.abs(harmonic)) / (np.mean(np.abs(percussive)) + 1e-6)

            # === 3. Spectral Flatness & ZCR ===
            flatness = np.mean(librosa.feature.spectral_flatness(y=y))
            zcr = np.mean(librosa.feature.zero_crossing_rate(y))

            # === 4. New: Low-frequency roll-off — piano hits lower than vocals
            rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85))

            print(f"[VDE] dB={mean_db:.2f}, std={std_db:.2f}, HPR={hpr:.2f}, Flat={flatness:.3f}, ZCR={zcr:.3f}, Rolloff={rolloff:.0f}")

            # === 5. Scoring ===
            score = 0
            if mean_db > -24: score += 1
            if std_db > 5: score += 1
            if hpr > 1.4: score += 1
            if flatness < 0.3: score += 1
            if 0.025 < zcr < 0.15: score += 1
            if rolloff > 3500: score += 1  # Vocals typically roll off > 3500Hz

            # Penalize very low-energy harmonic music (piano, ambient)
            if hpr > 2.8 and flatness < 0.35 and std_db < 6:
                print("[VDE] 🚫 Likely piano or ambient — overriding vocals")
                return False, 20

            confidence = round((score / 6) * 100)
            return confidence >= 60, confidence

        except Exception as e:
            print(f"[VDE] ❌ ERROR: {e}")
            return False, 0
