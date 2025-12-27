FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (build-essential needed for some python packages like asyncpg sometimes)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY deploy/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY config/ ./config/

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Run with Uvicorn for production-ready async support
CMD ["uvicorn", "src.web.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
