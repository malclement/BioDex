# Builder stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements
COPY requirements.txt .
RUN uv pip compile requirements.txt -o requirements.lock

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy compiled requirements
COPY --from=builder /app/requirements.lock .

# Install dependencies using UV
RUN uv pip install --system -r requirements.lock

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
