# Base image with Python 3.11
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies into virtualenv or globally
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install Node.js, OpenSSL and CA certificates (required by Prisma CLI and Query Engine)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    openssl \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app code
COPY app ./app
COPY prisma ./prisma
COPY .env* ./

# Initialize Prisma client generator (downloads correct Linux engine binary during build)
RUN prisma generate

EXPOSE 3000

ENV PORT=3000

# Start FastAPI application
CMD ["python", "-m", "app.main"]
