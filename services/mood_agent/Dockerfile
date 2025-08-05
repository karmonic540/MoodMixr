# services/mood_agent/Dockerfile

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "mood_agent_fastapi:app", "--host", "0.0.0.0", "--port", "8001"]
