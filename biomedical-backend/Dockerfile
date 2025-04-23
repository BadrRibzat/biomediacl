# Use official Python 3.11 slim image
   FROM python:3.11-slim

   # Set working directory
   WORKDIR /app

   # Copy requirements.txt
   COPY requirements.txt .

   # Install dependencies
   RUN pip install --no-cache-dir -r requirements.txt

   # Install libGL and libglib for OpenCV/MediaPipe
   RUN apt-get update && apt-get install -y \
       libgl1-mesa-glx \
       libglib2.0-0 \
       && rm -rf /var/lib/apt/lists/*

   # Copy application code
   COPY app/ ./app/

   # Expose port
   EXPOSE 8000

   # Health check to ensure Uvicorn is running
   HEALTHCHECK --interval=30s --timeout=3s \
       CMD curl -f http://localhost:8000/ || exit 1

   # Run uvicorn with workers for better reliability
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
