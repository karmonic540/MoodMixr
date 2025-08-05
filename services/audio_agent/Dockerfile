# services/audio_agent/Dockerfile

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "audio_agent_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
