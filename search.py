# search.py

import logging
from external_sources import fetch_from_other_sources
logger = logging.getLogger(__name__)

async def find_best_match(query: str, language: str = 'en') -> tuple:
    """
    Ищет определение термина исключительно из внешних источников.
    
    :param query: Термин для поиска.
    :param language: Язык запроса.
    :return: Кортеж (термин, определение) или (None, None) если не найдено.
    """
    query_lower = query.lower()

    try:
        # Получаем определение из внешних источников
        definition = await fetch_from_other_sources(query_lower, language=language)
        if definition:
            return query_lower, definition

        # Если определение не найдено
        logger.info(f"Термин '{query_lower}' не найден во внешних источниках.")
        return None, None
    except Exception as e:
        logger.error(f"Ошибка поиска термина: {e}")
        return None, None

def save_user_definition(term: str, definition: str):
    """
    Сохраняет пользовательское определение термина.
    (При необходимости можно хранить пользовательские определения в отдельной таблице.)
    
    :param term: Термин для сохранения.
    :param definition: Определение термина.
    """
    # Реализуйте логику сохранения пользовательских определений,
    # если вы хотите сохранять их отдельно.
    pass  # Удалено сохранение в глоссарий
