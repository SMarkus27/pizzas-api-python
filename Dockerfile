# Stage 1: Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment for dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime stage
FROM python:3.12-slim

# Create a non-root user to run the application
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Copy only the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code and set ownership
COPY --chown=appuser:appgroup main.py .
COPY --chown=appuser:appgroup src/ ./src/

# Ensure the appuser has access to the application directory
RUN chown appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
