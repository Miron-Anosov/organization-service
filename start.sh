#!/bin/sh
set -e

echo "Starting Gunicorn server..."
gunicorn --config /app/gunicorn_conf.py