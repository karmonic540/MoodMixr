FROM python:3.11-slim

# System libs for librosa/soundfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps
RUN pip install --no-cache-dir fastapi uvicorn librosa numpy soundfile python-multipart


# Copy in just this service (or rely on a bind mount during dev)
COPY . /app

# Make sure Python can import "services.*"
ENV PYTHONPATH=/app/..

EXPOSE 8000
CMD ["uvicorn", "services.audio_agent.audio_agent_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
