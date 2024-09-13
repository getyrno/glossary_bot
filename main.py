import logging
import asyncio
import os
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from ml.train_model import train_and_notify
from search import find_best_match, save_user_definition
from dotenv import load_dotenv
from telegram.helpers import escape_markdown

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TOKEN2 = os.getenv('TELEGRAM_BOT_TOKEN2')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")
    exit(1)
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN2 не установлен в переменных окружения.")
    exit(1)
if not CHAT_ID:
    logger.error("TELEGRAM_CHAT_ID не установлен в переменных окружения.")
    exit(1)

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
    user = update.effective_user
    query = update.message.text.strip()
    logger.info(f"Пользователь {user.id} отправил сообщение: {query}")

    if not query:
        await update.message.reply_text("Пожалуйста, введите корректный термин для поиска.")
        return

    term, definition = await find_best_match(query, language='ru')  # Предполагается, что язык русский
    if definition:
        term_escaped = escape_markdown(term.capitalize(), version=2)
        definition_escaped = escape_markdown(definition, version=2)
        
        logger.info(f"Найдено определение для термина '{term}': {definition}. Начинается вызов train_and_notify.")
        logger.info(f"Функция train_and_notify завершена для термина '{term_escaped}'.")

        response = f"*{term_escaped}*\n{definition_escaped}"
    else:
        response = "Термин не найден. Попробуйте другой запрос."

    try:
        await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN_V2)
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, train_and_notify, term_escaped, definition_escaped)

        logger.info(f"Отправлен ответ пользователю {user.id}: {response}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Функция смены языка пока не реализована.")
    logger.info(f"Пользователь {update.effective_user.id} попытался изменить язык.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('set_language', set_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Бот запущен и готов к работе.")
    application.run_polling()

if __name__ == '__main__':
   main()
