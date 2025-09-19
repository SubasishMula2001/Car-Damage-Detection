FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (for OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend package
COPY backend/ /app/backend/

# Copy frontend
COPY frontend/ /app/frontend/

EXPOSE 8000

# Run FastAPI app as a package
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
