FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY .idea/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .idea/app /app

RUN useradd -m appuser
USER appuser

EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1

CMD ["python", "main.py"]
