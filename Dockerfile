FROM python:3.10-slim

# -------------------------------------------------------------------
# Environment (Cloud Run safe)
# -------------------------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTORCH_ENABLE_MPS_FALLBACK=1 \
    MPLCONFIGDIR=/tmp/mpl

WORKDIR /app

# -------------------------------------------------------------------
# System dependencies (git is REQUIRED for CLIP)
# -------------------------------------------------------------------

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgl1 \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------
# Python dependencies
# -------------------------------------------------------------------

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------
# App code
# -------------------------------------------------------------------

COPY . .

# -------------------------------------------------------------------
# Server (Cloud Run optimized)
# -------------------------------------------------------------------

CMD ["gunicorn", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--workers", "1", \
     "--threads", "2", \
     "--timeout", "0", \
     "--bind", "0.0.0.0:8080", \
     "main:app"]
