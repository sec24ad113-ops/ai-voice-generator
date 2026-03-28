FROM python:3.10-slim

WORKDIR /app

# Install system dependencies needed by TTS
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create audio output folder
RUN mkdir -p static/audio

# Expose HuggingFace required port
EXPOSE 7860

# Start the app
CMD ["python", "app.py"]