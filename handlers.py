# handlers.py

import logging
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, filters
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode
from utils import get_language_keyboard, translate, get_error_message
from search import find_best_match, save_user_definition
from messages import GREETING_MESSAGE, MAIN_MESSAGE, LANGUAGES

logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
WAITING_FOR_DEFINITION = 1

# Управление языковыми предпочтениями
user_language_preferences = {}

async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        if user_id not in user_language_preferences:
            user_language_preferences[user_id] = 'en'  # Язык по умолчанию
            await update.message.reply_text(
                GREETING_MESSAGE['en'],
                reply_markup=get_language_keyboard()
            )
        else:
            preferred_language = user_language_preferences[user_id]
            await update.message.reply_text(MAIN_MESSAGE[preferred_language])
        logger.info(f"User {user_id} started the bot.")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text("An error occurred while processing your request.")

async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.from_user.id
    selected_language = query.data

    if selected_language in LANGUAGES:
        user_language_preferences[user_id] = selected_language
        greeting_message = MAIN_MESSAGE[selected_language]
        await query.answer()
        await query.edit_message_text(greeting_message, reply_markup=None)
        logger.info(f"User {user_id} changed language to {LANGUAGES[selected_language]}.")
    else:
        await query.answer(
            text=get_error_message(
                'unsupported_language',
                'en',
                language=selected_language,
                supported=', '.join(LANGUAGES.keys())
            )
        )

async def set_language(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if context.args:
        new_language = context.args[0]
        if new_language in LANGUAGES:
            user_language_preferences[user_id] = new_language
            response = MAIN_MESSAGE[new_language]
        else:
            response = get_error_message(
                'unsupported_language',
                user_language_preferences.get(user_id, 'en'),
                language=new_language,
                supported=', '.join(LANGUAGES.keys())
            )
    else:
        response = "Please specify a language code. For example, /language en."

    await update.message.reply_text(response)
    logger.info(f"User {user_id} changed language to {user_language_preferences.get(user_id, 'en')}.")

async def find_term(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    query = update.message.text.strip()
    preferred_language = user_language_preferences.get(user_id, 'en')

    try:
        # Переводим запрос на английский для поиска
        translated_query = translate(query, 'en', preferred_language)

        # Ищем термин и получаем описание
        term, description = await find_best_match(translated_query, language='en')

        if term and description:
            # Переводим термин и описание на предпочтительный язык
            translated_term = translate(term, preferred_language, 'en')
            translated_description = translate(description, preferred_language, 'en')

            # Экранируем специальные символы
            translated_term = escape_markdown(translated_term, version=2)
            translated_description = escape_markdown(translated_description, version=2)

            response = f"*{translated_term}*\n\n{translated_description}"
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            response = get_error_message('term_not_found', preferred_language, term=query)
            response += "\nWould you like to provide a definition for this term? (yes/no)"
            await update.message.reply_text(response)
            # Сохраняем состояние ожидания определения
            context.user_data['awaiting_definition'] = True
            context.user_data['term_to_define'] = query
            return WAITING_FOR_DEFINITION
    except Exception as e:
        logger.error(f"Error finding term: {e}")
        response = get_error_message('general_error', preferred_language, error=str(e))
        await update.message.reply_text(response)

    logger.info(f"User {user_id} sent a message: {query}")
    logger.info(f"Response sent to user {user_id}: {response}")
    return ConversationHandler.END

async def receive_definition(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_response = update.message.text.strip().lower()
    preferred_language = user_language_preferences.get(user_id, 'en')
    term = context.user_data.get('term_to_define')

    if user_response in ['yes', 'да']:
        await update.message.reply_text("Please provide the definition for the term.")
        return WAITING_FOR_DEFINITION
    elif user_response in ['no', 'нет']:
        await update.message.reply_text("Alright, if you have any other questions, feel free to ask!")
        context.user_data['awaiting_definition'] = False
        context.user_data.pop('term_to_define', None)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please reply with 'yes' or 'no'.")
        return WAITING_FOR_DEFINITION

async def save_definition(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    definition = update.message.text.strip()
    term = context.user_data.get('term_to_define')
    preferred_language = user_language_preferences.get(user_id, 'en')

    try:
        save_user_definition(term, definition)
        response = f"Thank you! The definition for '{term}' has been added."
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error saving user definition: {e}")
        response = get_error_message('general_error', preferred_language, error=str(e))
        await update.message.reply_text(response)

    # Очистка состояния
    context.user_data['awaiting_definition'] = False
    context.user_data.pop('term_to_define', None)
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Operation cancelled.")
    context.user_data['awaiting_definition'] = False
    context.user_data.pop('term_to_define', None)
    return ConversationHandler.END
