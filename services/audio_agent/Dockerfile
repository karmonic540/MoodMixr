# Dockerfile for audio-agent

FROM python:3.10-slim

# Install system deps for audio decoding
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY audio_agent_fastapi.py .
COPY audio_logic.py .

EXPOSE 8001

CMD ["uvicorn", "audio_agent_fastapi:app", "--host", "0.0.0.0", "--port", "8001"]
