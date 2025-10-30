# # Recommended Dockerfile (uses package layout: backend/ as a package)
# FROM python:3.11-slim

# WORKDIR /app

# # Install small runtime deps needed for opencv headless
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgl1 \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements first to leverage cache
# COPY backend/requirements.txt /app/requirements.txt

# # Install python deps exactly as pinned in requirements.txt
# RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# # Copy backend as a package and frontend
# COPY backend/ /app/backend/
# COPY frontend/ /app/frontend/

# EXPOSE 8000

# # Run uvicorn pointing to the package module (this matches your code layout)
# CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
# Use an official PyTorch CPU image (small, prebuilt PyTorch wheel)
# Dockerfile - slim, pip-based approach
# FROM python:3.11-slim

# WORKDIR /app

# # runtime deps for opencv etc.
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgl1 libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# # copy only requirements first to leverage cache
# COPY backend/requirements.txt /app/requirements.txt

# # install pip deps (no cache)
# RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

# # copy application
# COPY backend/ /app/backend/
# COPY frontend/ /app/frontend/

# RUN mkdir -p /app/backend/server_captures /app/backend/data/processed

# EXPOSE 8000
# CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates libjpeg-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install --no-cache-dir --prefix=/install -r /app/requirements.txt

FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/

RUN mkdir -p /app/backend/server_captures /app/backend/data/processed

EXPOSE 8000
CMD ["uvicorn","backend.app:app","--host","0.0.0.0","--port","8000"]