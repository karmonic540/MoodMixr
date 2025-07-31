# services/mood_agent/Dockerfile

FROM python:3.10-slim

# Install system dependencies for audio decoding (FLAC, MP3, etc.)
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mood_agent_fastapi.py .
COPY mood_logic.py .

EXPOSE 8000

CMD ["uvicorn", "mood_agent_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
