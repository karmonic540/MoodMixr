# App Dockerfile
FROM python:3.10-slim

# System deps for librosa / soundfile / ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ffmpeg libsndfile1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy repo
COPY . .

ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

EXPOSE 8501
CMD ["streamlit","run","app/moodmixr_app.py","--server.port=8501","--server.address=0.0.0.0"]
