#translator
from deep_translator import GoogleTranslator
# Создаем объект для перевода
translator = GoogleTranslator()

# Поддерживаемые языки
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

# Сообщения об ошибках на разных языках
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

# Функция для получения сообщения об ошибке на выбранном языке
def get_error_message(error_type, user_language, **kwargs):
    # Если язык пользователя не поддерживается, используем английский по умолчанию
    if user_language not in ERROR_MESSAGES[error_type]:
        user_language = 'en'
    return ERROR_MESSAGES[error_type][user_language].format(**kwargs)

# Функция для перевода текста на указанный язык
# Пример синхронного вызова
def translate(text, target_language, user_language):
    # Проверяем, поддерживается ли целевой язык
    if target_language not in LANGUAGES:
        supported_languages = ', '.join(LANGUAGES.keys())
        return get_error_message('unsupported_language', user_language, language=target_language, supported=supported_languages)

    try:
        # Выполняем перевод
        translation = translator.translate(text, dest=target_language)
        return translation.text  # Возвращаем текст перевода
    except Exception as e:
        # В случае ошибки возвращаем сообщение об ошибке
        return get_error_message('translation_error', user_language, error=str(e))
