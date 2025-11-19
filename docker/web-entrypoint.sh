#!/usr/bin/env sh
set -eu

echo "[$(date --iso-8601=seconds)] Running database migrations..."
uv run python src/manage.py migrate --noinput
echo "[$(date --iso-8601=seconds)] Migrations completed successfully."

echo "[$(date --iso-8601=seconds)] Starting application: $*"
exec "$@"
