FROM python:3.11-slim

WORKDIR /app

COPY .idea/requirements.txt .
RUN pip install --no-cache-dir -r .idea/requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]