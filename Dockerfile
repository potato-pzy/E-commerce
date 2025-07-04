# Use specific Python version
FROM python:3.12-slim

# Install system dependencies for Pillow and psycopg2 (Postgres)
RUN apt-get update && \
    apt-get install -y libjpeg-dev zlib1g-dev gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first and install (for Docker cache efficiency)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Collect static files at build time (optional: can also run in entrypoint)
RUN python manage.py collectstatic --noinput

# Expose port (Render expects the app to bind to $PORT)
EXPOSE 8000

# Use environment variable for Django settings (if you have different settings for prod/dev)
# ENV DJANGO_SETTINGS_MODULE=E-commerce.settings

# Entrypoint: Run migrations, then start server
CMD ["sh", "-c", "python manage.py migrate && python create_superuser.py && gunicorn grocery_ecommerce.wsgi:application --bind 0.0.0.0:8000"]
