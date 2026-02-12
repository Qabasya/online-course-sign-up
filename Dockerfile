FROM python:3.11-slim

# Не даем Python писать .pyc файлы и заставляем сразу выводить логи в консоль
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем папки заранее (на случай, если не используем volumes)
RUN mkdir -p logs db

CMD ["python", "main.py"]