import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN2')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

logging.info(f"TOKEN: {TOKEN}")
logging.info(f"CHAT_ID: {CHAT_ID}")

def send_message(text):
    if not TOKEN or not CHAT_ID:
        logging.error("Отсутствуют необходимые переменные окружения (TOKEN или CHAT_ID)")
        return

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }

    response = None

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        logging.info(f"Сообщение отправлено: {text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")
        if response is not None:
            logging.error(f"Ответ от Telegram: {response.text}")
 