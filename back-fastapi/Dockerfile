FROM python:3.12-slim

# Set a working directory
WORKDIR /app

# Environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system deps (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose port
EXPOSE 8000

# Healthcheck (use stdlib so it doesn't depend on requests being installed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import http.client,sys; c=http.client.HTTPConnection('localhost',8000,timeout=5); c.request('GET','/health'); r=c.getresponse(); sys.exit(0 if r.status==200 else 1)" || exit 1

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]