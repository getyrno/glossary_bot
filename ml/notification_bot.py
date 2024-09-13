import os
import logging
from telegram import Bot
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение токена и chat_id из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN2')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Инициализация бота
bot = Bot(token=TOKEN)

def send_message(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
        logging.info(f"Сообщение успешно отправлено: {text}")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения: {e}")

if __name__ == "__main__":
    send_message("Тестовое сообщение для проверки")
