# --- base image ---
FROM python:3.12-slim

# --- system setup ---
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# --- dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- app source ---
COPY . .

WORKDIR /app/src

# --- runtime ---
ENV DJANGO_SETTINGS_MODULE=echofield.settings
CMD ["gunicorn", "echofield.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
