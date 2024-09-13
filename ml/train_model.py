import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from ml.utils import preprocess_term, vectorize_terms
from ml.classifier import classify_term_context_async
from ml.notification_bot import send_message
from ml.analysis import analyze_term_searches, visualize_recommendations
import pandas as pd


logging.basicConfig(level=logging.INFO)

# Экзекьютор для выполнения в фоне
executor = ThreadPoolExecutor(max_workers=1)

async def train_and_notify(term, definition, elapsed_time):
    """
    Асинхронная функция для обработки термина и уведомления.
    """
    try:
        await process_term(term, definition, elapsed_time)
    except Exception as exc:
        logging.error(f'Обработка термина "{term}" вызвала исключение: {exc}')

async def process_term(term, definition, elapsed_time):
    """
    Асинхронная функция для обработки термина.
    """
    logging.info(f"Начинается обработка термина '{term}'")

    # Предобработка термина
    processed_term = preprocess_term(term)
    logging.info(f"Предобработанный термин: {processed_term}")

    # Векторизация термина
    terms = [processed_term]
    term_vectors = vectorize_terms(terms)
    logging.info(f"Векторизация завершена для термина: {processed_term}")

    try:
        # Ожидание результата классификации
        context = await classify_term_context_async(processed_term, definition)
        logging.info(f"Контекст для термина '{term}' определен как: {context}")
    except Exception as e:
        logging.error(f"Ошибка при классификации термина '{term}': {e}")
        await send_message(f"Ошибка классификации термина '{term}': {e}")
        return

    # Генерация отчета
    report = (f"Термин: {term}\n"
              f"Предсказанный контекст: {context}\n"
              f"Сгенерированное определение: В разработке\n"
              f"Отправленное определение: {definition}\n"
              f"Время от получения сообщения до отправки ответа: {elapsed_time:.2f} секунд")
    
    try:
        await send_message(report)
        logging.info(f"Отчет успешно отправлен для термина '{term}'")
    except Exception as e:
        logging.error(f"Ошибка при отправке отчета для термина '{term}': {e}")

def start_task(term, definition, elapsed_time):
    """
    Запуск асинхронной задачи из потока.
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(train_and_notify(term, definition, elapsed_time))
