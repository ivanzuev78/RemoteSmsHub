# Используем официальный образ Python в качестве базового
FROM python:3.11-slim as base

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM base as build
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
