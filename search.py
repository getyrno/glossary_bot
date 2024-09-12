# search.py

import logging
import os
import json
from external_sources import fetch_from_other_sources

logger = logging.getLogger(__name__)

# Файл глоссария используется как кэш
glossary_file = 'my_glossary.json'

# Если файла нет, создаём пустой глоссарий
if not os.path.exists(glossary_file):
    with open(glossary_file, 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=4)
    logger.info(f"Создан новый глоссарий: {glossary_file}")

def save_user_definition(term: str, definition: str):
    """
    Сохраняет пользовательское определение термина в глоссарий (кэш).
    
    :param term: Термин для сохранения.
    :param definition: Определение термина.
    """
    term_lower = term.lower()

    # Загружаем кэш (глоссарий)
    try:
        with open(glossary_file, 'r', encoding='utf-8') as f:
            glossary = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка загрузки глоссария: {e}")
        glossary = {}

    # Сохраняем определение
    glossary[term_lower] = definition
    try:
        with open(glossary_file, 'w', encoding='utf-8') as f:
            json.dump(glossary, f, ensure_ascii=False, indent=4)
        logger.info(f"Пользовательский термин '{term_lower}' сохранён в кэш.")
    except Exception as e:
        logger.error(f"Ошибка сохранения глоссария: {e}")

async def find_best_match(query: str, language: str = 'en') -> tuple:
    """
    Ищет лучшее соответствие для запроса в кэше или внешних источниках.
    
    :param query: Термин для поиска.
    :param language: Язык запроса.
    :return: Кортеж (термин, определение) или (None, None) если не найдено.
    """
    query_lower = query.lower()

    # Загружаем кэш (глоссарий)
    try:
        with open(glossary_file, 'r', encoding='utf-8') as f:
            glossary = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка загрузки глоссария: {e}")
        glossary = {}

    # Проверяем, есть ли термин в кэше
    if query_lower in glossary:
        logger.info(f"Термин '{query_lower}' найден в кэше.")
        return query_lower, glossary[query_lower]

    # Если термин не в кэше, получаем определение из внешних источников
    try:
        definition = await fetch_from_other_sources(query_lower, language=language)
    except Exception as e:
        logger.error(f"Ошибка при получении определения из внешних источников: {e}")
        definition = None

    if definition:
        # Сохраняем термин и его определение в кэше
        glossary[query_lower] = definition
        try:
            with open(glossary_file, 'w', encoding='utf-8') as f:
                json.dump(glossary, f, ensure_ascii=False, indent=4)
            logger.info(f"Термин '{query_lower}' получен из внешних источников и сохранён в кэше.")
        except Exception as e:
            logger.error(f"Ошибка сохранения глоссария: {e}")
        return query_lower, definition

    # Если определение не найдено
    logger.info(f"Термин '{query_lower}' не найден во внешних источниках.")
    return None, None
