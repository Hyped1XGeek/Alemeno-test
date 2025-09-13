# Use Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Copy project files first (including README.md)
COPY . .

# Install Python dependencies
RUN uv pip install --system -e .

# Create logs directory
RUN mkdir -p logs

# Create staticfiles directory
RUN mkdir -p staticfiles

# Create templates directory
RUN mkdir -p templates

# Collect static files (if any)
RUN python manage.py collectstatic --noinput --clear || true

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Wait for PostgreSQL to be ready\n\
echo "Waiting for PostgreSQL..."\n\
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do\n\
  echo "PostgreSQL is unavailable - sleeping"\n\
  sleep 1\n\
done\n\
echo "PostgreSQL is up - executing command"\n\
\n\
# Run migrations\n\
echo "Running database migrations..."\n\
python manage.py migrate\n\
\n\
# Import initial data if it exists\n\
if [ -f "Docs/customer_data.csv" ] && [ -f "Docs/loan_data.csv" ]; then\n\
    echo "Importing initial data..."\n\
    python manage.py import_data --customer-file Docs/customer_data.csv --loan-file Docs/loan_data.csv\n\
fi\n\
\n\
# Execute the main command\n\
exec "$@"' > /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]