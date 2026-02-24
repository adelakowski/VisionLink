FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements_gradio.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_gradio.txt

# Copy source code
COPY src/ ./src/
# Copy environments if needed
COPY .env* ./

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7860
EXPOSE 7860

# Run the application
CMD ["python", "src/ui_gradio.py"]
