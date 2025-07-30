# ⛩️ MoodMixr by Karmonic (Akshaykumarr Surti)
# 🌐 A fusion of AI + Human creativity, built with sacred precision.
# 🧠 Modular Agent-Based Architecture | 🎵 Pro DJ Tools | ⚛️ Future Sound Intelligence
import os
import tempfile
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

class YouTubeFallbackAgent:
    @staticmethod
    def download_audio(query: str) -> tuple[str, str] | tuple[None, None]:
        """
        Downloads the best audio version of the first YouTube search result.

        Args:
            query (str): Search term (e.g., track name + artist).

        Returns:
            (str, str): Tuple of (file_path, video_url), or (None, None) on failure.
        """
        try:
            print(f"[YouTubeFallbackAgent] Searching for: {query}")
            results = YoutubeSearch(query, max_results=1).to_dict()
            if not results:
                print("[YouTubeFallbackAgent] No results found.")
                return None, None

            url_suffix = results[0]["url_suffix"]
            url = f"https://www.youtube.com{url_suffix}"
            print(f"[YouTubeFallbackAgent] Downloading from: {url}")

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': temp_file.name,
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                }],
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"[YouTubeFallbackAgent] Download complete: {temp_file.name}")
            return temp_file.name, url

        except Exception as e:
            print(f"[YouTubeFallbackAgent] Error during download: {e}")
            return None, None
