#!/bin/bash

export DJANGO_SETTINGS_MODULE=product_store.settings
export PYTHONPATH=/app/metadata_store:/app/auth_app:/app

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Populate data..."
python manage.py populate_data

