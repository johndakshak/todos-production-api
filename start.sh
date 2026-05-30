#!/bin/bash

echo "Running database migrations..."
cd /app
alembic upgrade head

echo "Migrations completed successfully!"
echo "Starting application..."

exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
