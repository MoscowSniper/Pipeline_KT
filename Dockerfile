FROM python:3.11-slim

WORKDIR /app

# Копируем всю папку .idea
COPY .idea/ .idea/

# Устанавливаем зависимости из .idea/requirements.txt
RUN pip install --no-cache-dir -r .idea/requirements.txt

# Копируем остальные файлы
COPY . .

EXPOSE 8000

CMD ["python", "main.py"]