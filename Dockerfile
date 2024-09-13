FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
