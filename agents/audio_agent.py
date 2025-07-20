import librosa
from librosa.beat import tempo
import numpy as np

class AudioAnalyzerAgent:

    @staticmethod
    def analyze(track_path):
        try:
            y, sr = librosa.load(track_path)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            key = chroma.mean(axis=1).argmax()

            # Map index to musical key
            key_map = ['C', 'C#', 'D', 'D#', 'E', 'F', 
                       'F#', 'G', 'G#', 'A', 'A#', 'B']
            musical_key = key_map[key % 12]

            import numpy as np
            return int(np.round(tempo)), musical_key


        except Exception as e:
            print(f"[AudioAnalyzerAgent] Error: {e}")
            return None, None
