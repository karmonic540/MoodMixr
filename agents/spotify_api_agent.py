# ⛩️ MoodMixr Utility Core
# 🎛️ Built by Karmonic for sacred creative intelligence and modular clarity
# 🧠 Purpose: Handle audio processing, mood detection, waveform rendering, transition logic, and platform sync
# Created: 2025-07-21 | License: MIT + Karma Clause
import requests
import streamlit as st


class SpotifyApiAgent:
    def __init__(self):
        self.client_id = st.secrets["SPOTIFY_CLIENT_ID"]
        self.client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]
        self.token = self._get_token()

    def _get_token(self):
        auth_url = "https://accounts.spotify.com/api/token"
        auth_data = {"grant_type": "client_credentials"}
        auth_response = requests.post(
            auth_url, data=auth_data, auth=(self.client_id, self.client_secret)
        )
        return auth_response.json().get("access_token")

    def search(self, query, types="track", limit=5):
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"q": query, "type": types, "limit": limit}
        res = requests.get(
            "https://api.spotify.com/v1/search", headers=headers, params=params
        )
        return res.json()

    def get_audio_features(self, track_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        res = requests.get(url, headers=headers)
        return res.json()
