# 🔄 MoodMixr Agent: Transition Recommender
# 🔱 Guided by Lord Shiva — the cosmic transformer of rhythm, flow, and intention.
# 🎧 Suggests divine transitions between tracks based on BPM, energy, and emotional mood.
# © 2025 Karmonic | MoodMixr Signature Embedded

from utils.utils import get_spotify_token, search_spotify_track, get_spotify_audio_features

class DiscoverAgent:
    @staticmethod
    def fetch_tracks(query):
        token = get_spotify_token()
        results = search_spotify_track(query, token)
        enriched = []

        for track in results:
            features = get_spotify_audio_features(track["id"], token)
            if features:
                bpm = round(features.get("tempo", 0))
                key = features.get("key", "Unknown")
                energy = round(features.get("energy", 0.0), 2)
                danceability = round(features.get("danceability", 0.0), 2)

                mood = "Energetic" if energy > 0.6 else "Chill" if energy < 0.3 else "Groovy"

                enriched.append({
                    "name": track["name"],
                    "artist": track["artist"],
                    "album": track["album"],
                    "image": track["image"],
                    "preview_url": track["preview_url"],
                    "id": track["id"],
                    "bpm": bpm,
                    "key": key,
                    "energy": energy,
                    "mood": mood
                })
        return enriched
