# search.py

import logging
from external_sources import fetch_from_other_sources
logger = logging.getLogger(__name__)

async def find_best_match(query: str, language: str = 'en') -> tuple:
    query_lower = query.lower()

    try:
        definition = await fetch_from_other_sources(query_lower, language=language)
        if definition:
            return query_lower, definition
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
    pass  # Удалено сохранение в глоссарий
