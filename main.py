import logging
import asyncio
import os
import time  # Для измерения времени
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from ml.train_model import start_task
from search import find_best_match
from dotenv import load_dotenv
from telegram.helpers import escape_markdown
from concurrent.futures import ThreadPoolExecutor

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена и ID чата из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")
    exit(1)
if not CHAT_ID:
    logger.error("TELEGRAM_CHAT_ID не установлен в переменных окружения.")
    exit(1)

# Экзекьютор для фоновых задач (уменьшаем количество потоков для снижения нагрузки)
executor = ThreadPoolExecutor(max_workers=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start.
    """
    user = update.effective_user
    await update.message.reply_text(
        f'Привет, {user.first_name}! Я бот для поиска терминов. Введите термин, чтобы получить его определение.'
    )
    logger.info(f"Пользователь {user.id} начал взаимодействие с ботом.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик входящих сообщений. Добавляет запросы для фона.
    """
    # Начинаем отслеживать время выполнения задачи
    start_time = time.time()

    user = update.effective_user
    query = update.message.text.strip()
    logger.info(f"Пользователь {user.id} отправил сообщение: {query}")

    if not query:
        await update.message.reply_text("Пожалуйста, введите корректный термин для поиска.")
        return

    # Поиск термина и его определения
    term, definition = await find_best_match(query, language='ru')
    if definition:
        term_escaped = escape_markdown(term.capitalize(), version=2)
        definition_escaped = escape_markdown(definition, version=2)
        
        logger.info(f"Найдено определение для термина '{term}': {definition}.")
        
        response = f"*{term_escaped}*\n{definition_escaped}"
    else:
        response = "Термин не найден. Попробуйте другой запрос."

    # Отправка ответа пользователю
    try:
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN_V2)
        
        # Завершаем измерение времени
        elapsed_time = time.time() - start_time
        logger.info(f"Ответ отправлен пользователю за {elapsed_time:.2f} секунд.")

        # Логируем время выполнения
        logger.info(f"Время от получения сообщения до отправки ответа: {elapsed_time:.2f} секунд")
        
        # Добавляем задачу для фона без ожидания завершения
        asyncio.create_task(process_task(term_escaped, definition_escaped, elapsed_time))
        
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

async def process_task(term, definition, elapsed_time):
    """
    Обрабатывает задачу в фоновом режиме и передаёт время выполнения в train_and_notify.
    """
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(executor, start_task, term, definition, elapsed_time)
        logger.info(f"Функция start_task завершена для термина '{term}'.")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке термина '{term}': {e}")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Временный обработчик смены языка.
    """
    await update.message.reply_text("Функция смены языка пока не реализована.")
    logger.info(f"Пользователь {update.effective_user.id} попытался изменить язык.")

def main():
    """
    Основная функция для запуска бота.
    """
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('set_language', set_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен и готов к работе.")

    # Запускаем основное приложение для обработки событий Telegram
    application.run_polling()

if __name__ == '__main__':
    main()
