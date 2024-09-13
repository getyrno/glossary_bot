import logging
import asyncio
import os
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from ml.train_model import train_and_notify
from search import find_best_match
from dotenv import load_dotenv
from telegram.helpers import escape_markdown
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")
    exit(1)
if not CHAT_ID:
    logger.error("TELEGRAM_CHAT_ID не установлен в переменных окружения.")
    exit(1)

# Очередь для задач
task_queue = asyncio.Queue()

# Экзекьютор для фоновых задач (чтобы не блокировать основной поток)
executor = ThreadPoolExecutor(max_workers=4)

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
    Обработчик входящих сообщений. Добавляет запросы в очередь.
    """
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
        
        logger.info(f"Найдено определение для термина '{term}': {definition}. Добавление задачи в очередь.")
        
        response = f"*{term_escaped}*\n{definition_escaped}"
    else:
        response = "Термин не найден. Попробуйте другой запрос."

    # Отправка ответа пользователю
    try:
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN_V2)
        
        # Добавляем задачу для фона
        await task_queue.put((term_escaped, definition_escaped))
        
        logger.info(f"Задача для термина '{term}' добавлена в очередь.")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

async def worker():
    """
    Рабочий процесс для обработки задач из очереди. Будет работать асинхронно в фоне.
    """
    while True:
        term, definition = await task_queue.get()
        try:
            # Асинхронно выполняем train_and_notify в отдельном потоке через executor
            await asyncio.get_event_loop().run_in_executor(executor, train_and_notify, [(term, definition)])
        except Exception as e:
            logger.error(f"Ошибка при обработке термина '{term}': {e}")
        finally:
            task_queue.task_done()

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Временный обработчик смены языка.
    """
    await update.message.reply_text("Функция смены языка пока не реализована.")
    logger.info(f"Пользователь {update.effective_user.id} попытался изменить язык.")

async def start_workers(n=3):
    """
    Функция для запуска нескольких рабочих процессов (workers) для обработки очереди.
    """
    for i in range(n):
        logger.info(f"Запуск рабочего процесса {i + 1}")
        asyncio.create_task(worker())

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

    # Запускаем рабочие процессы
    loop = asyncio.get_event_loop()
    loop.create_task(start_workers())

    # Запускаем основное приложение для обработки событий Telegram
    application.run_polling()

if __name__ == '__main__':
    main()
