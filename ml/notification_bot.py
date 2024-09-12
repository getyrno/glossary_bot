# ml/notification_bot.py
import os
import requests
import logging
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение токена и chat_id из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN2')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_message(text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }

    response = None  # Инициализация переменной

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        logging.info(f"Сообщение отправлено: {text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
        if response is not None:
            logging.error(f"Ответ от Telegram: {response.text}")
