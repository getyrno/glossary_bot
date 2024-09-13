#translator
from deep_translator import GoogleTranslator
translator = GoogleTranslator()

LANGUAGES = {
    'ru': 'Русский',
    'en': 'Английский',
    'es': 'Испанский',
    'fr': 'Французский',
    'de': 'Немецкий',
    'it': 'Итальянский',
    'zh-cn': 'Китайский (упрощенный)',
    'ja': 'Японский',
    'ko': 'Корейский',
}

ERROR_MESSAGES = {
    'unsupported_language': {
        'en': "Language {language} is not supported. Please choose one of the supported languages: {supported}.",
        'ru': "Язык {language} не поддерживается. Пожалуйста, выберите один из поддерживаемых языков: {supported}.",
        'es': "El idioma {language} no es compatible. Por favor elige uno de los idiomas compatibles: {supported}.",
        'fr': "La langue {language} n'est pas supportée. Veuillez choisir une des langues supportées: {supported}.",
        'de': "Die Sprache {language} wird nicht unterstützt. Bitte wählen Sie eine der unterstützten Sprachen: {supported}.",
        'it': "La lingua {language} non è supportata. Scegli una delle lingue supportate: {supported}.",
    },
    'translation_error': {
        'en': "Translation error: {error}",
        'ru': "Ошибка перевода: {error}",
        'es': "Error de traducción: {error}",
        'fr': "Erreur de traduction: {error}",
        'de': "Übersetzungsfehler: {error}",
        'it': "Errore di traduzione: {error}",
    }
}

def get_error_message(error_type, user_language, **kwargs):
    if user_language not in ERROR_MESSAGES[error_type]:
        user_language = 'en'
    return ERROR_MESSAGES[error_type][user_language].format(**kwargs)

def translate(text, target_language, user_language):
    if target_language not in LANGUAGES:
        supported_languages = ', '.join(LANGUAGES.keys())
        return get_error_message('unsupported_language', user_language, language=target_language, supported=supported_languages)

    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        return get_error_message('translation_error', user_language, error=str(e))
