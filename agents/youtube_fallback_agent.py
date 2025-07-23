import os
import tempfile
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

class YouTubeFallbackAgent:
    @staticmethod
    def download_audio(query: str) -> str:
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            if not results:
                return None
            url_suffix = results[0]["url_suffix"]
            url = f"https://www.youtube.com{url_suffix}"

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

            return temp_file.name
        except Exception as e:
            print(f"[YouTubeFallbackAgent] Error: {e}")
            return None
