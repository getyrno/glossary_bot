# utils.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from deep_translator import GoogleTranslator
import logging
from telegram.helpers import escape_markdown
logger = logging.getLogger(__name__)

LANGUAGES = {
    'ru': 'Русский',
    'en': 'English',
    'zh-cn': '中文（简体）',
}

ERROR_MESSAGES = {
    'unsupported_language': {
        'en': "Language '{language}' is not supported. Please choose one of the supported languages: {supported}.",
        'ru': "Язык '{language}' не поддерживается. Пожалуйста, выберите один из поддерживаемых языков: {supported}.",
        'zh-cn': "语言 '{language}' 不受支持。请从受支持的语言中选择一个: {supported}。",
    },
    'translation_error': {
        'en': "Translation error: {error}",
        'ru': "Ошибка перевода: {error}",
        'zh-cn': "翻译错误: {error}",
    },
    'term_not_found': {
        'en': "Term '{term}' not found. Please try another term.",
        'ru': "Термин '{term}' не найден. Пожалуйста, попробуйте другой термин.",
        'zh-cn': "术语 '{term}' 未找到。请尝试其他术语。",
    },
    'general_error': {
        'en': "An error occurred: {error}",
        'ru': "Произошла ошибка: {error}",
        'zh-cn': "发生错误: {error}",
    }
}

def get_error_message(error_type: str, user_language: str, **kwargs) -> str:
    if error_type not in ERROR_MESSAGES:
        return "An unknown error occurred."
    
    user_language = user_language if user_language in ERROR_MESSAGES[error_type] else 'en'
    for key, value in kwargs.items():
        if isinstance(value, str):
            kwargs[key] = escape_markdown(value, version=2)
    return ERROR_MESSAGES[error_type][user_language].format(**kwargs)

def get_language_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton('🇷🇺 Русский', callback_data='ru')],
        [InlineKeyboardButton('🇬🇧 English', callback_data='en')],
        [InlineKeyboardButton('🇨🇳 中文', callback_data='zh-cn')]
    ]
    return InlineKeyboardMarkup(keyboard)

def translate(text: str, target_language: str, source_language: str = 'en') -> str:
    if target_language not in LANGUAGES:
        supported_languages = ', '.join(LANGUAGES.keys())
        logger.error(f"Unsupported language: {target_language}")
        return text

    try:
        translator = GoogleTranslator(source=source_language, target=target_language)
        return translator.translate(text)
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text
