
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements_gradio.txt ./

# Install dependencies
# Note: Combining them to ensure no conflicts, though pip handles it.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_gradio.txt
RUN pip install --no-cache-dir keras-nlp keras

# Copy source code
COPY src/ ./src/
COPY .env ./
# Copy local data/archives if necessary, but ideally these should be in cloud storage
# For now, we assume the app might need some local files if they are small.
# Given the size of "archive.zip" (1.7GB), we DO NOT want to copy that into the image.
# We copy only necessary source files.

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port
ENV PORT=7860
EXPOSE 7860

# Run the application
CMD ["python", "src/ui_gradio.py"]
