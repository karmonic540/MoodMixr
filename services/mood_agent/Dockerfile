FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn librosa numpy soundfile python-multipart

COPY . /app

ENV PYTHONPATH=/app/..
EXPOSE 8001
CMD ["uvicorn", "services.mood_agent.mood_agent_fastapi:app", "--host", "0.0.0.0", "--port", "8001"]
