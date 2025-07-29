# /Secure-vault-backend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and group
RUN addgroup --system app && adduser --system --group app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directories and set ownership to the new user
# This is more secure than chmod 777
RUN mkdir -p media staticfiles data && \
    chown -R app:app /app

# Switch to the non-root user
USER app

# Make start script executable (already owned by 'app' user from chown)
# No need for chmod +x if permissions are set correctly in git
# But it's safe to keep it.
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]