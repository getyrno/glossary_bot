# main.py

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
from search import find_best_match, save_user_definition
from dotenv import load_dotenv
from telegram.helpers import escape_markdown

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN не установлен в переменных окружения.")
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
    """
    Обработчик текстовых сообщений.
    """
    user = update.effective_user
    query = update.message.text.strip()
    logger.info(f"Пользователь {user.id} отправил сообщение: {query}")

    if not query:
        await update.message.reply_text("Пожалуйста, введите корректный термин для поиска.")
        return

    term, definition = await find_best_match(query, language='ru')  # Предполагается, что язык русский
    if definition:
        # Экранируем специальные символы для MarkdownV2
        term_escaped = escape_markdown(term.capitalize(), version=2)
        definition_escaped = escape_markdown(definition, version=2)
        response = f"*{term_escaped}*\n{definition_escaped}"
    else:
        response = "Термин не найден. Попробуйте другой запрос."

    await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN_V2)
    logger.info(f"Отправлен ответ пользователю {user.id}: {response}")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /set_language для изменения языка поиска.
    """
    # Реализация смены языка по вашему усмотрению
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
    application.run_polling()

if __name__ == '__main__':
   main()