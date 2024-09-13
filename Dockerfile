FROM python:3.10-slim

WORKDIR /app

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y build-essential

# Копируем файл зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

CMD ["python", "main.py"]
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
