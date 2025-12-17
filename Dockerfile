FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ALL source files (including README.md needed by pyproject.toml)
COPY . .

# Expose port for HTTP transport
ENV PORT=8000
EXPOSE 8000

# Run the HTTP server for Railway
CMD ["python", "-m", "src.http_server"]
