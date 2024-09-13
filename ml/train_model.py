import logging
from .classifier import classify_term_context
from .notification_bot import send_message

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

def train_and_notify(term, definition):
    logging.info(f"Начинаем классификацию для термина: {term}")
    
    # Классифицируем контекст термина
    try:
        context = classify_term_context(term, definition)
        logging.info(f"Контекст для термина '{term}' определен как: {context}")
    except Exception as e:
        logging.error(f"Ошибка при классификации термина '{term}': {e}")
        return
    
    # Отправляем результаты в мониторингового бота
    try:
        send_message(f"Term: {term}\nPredicted Context: {context}")
        logging.info(f"Сообщение успешно отправлено для термина '{term}' с контекстом '{context}'")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения для термина '{term}': {e}")
