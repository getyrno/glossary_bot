# external_sources.py

import httpx
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'TelegramBot/1.0 (https://github.com/yourusername/yourbot)'
}

async def fetch_from_wikipedia(term: str, language: str = 'en') -> str:
    try:
        term_encoded = quote(term)
        url = f'https://{language}.wikipedia.org/api/rest_v1/page/summary/{term_encoded}'
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            extract = data.get('extract')
            if extract:
                return extract
            else:
                return await search_wikipedia(term, language)
        elif response.status_code == 404:
            return await search_wikipedia(term, language)
        else:
            logger.error(f'Wikipedia API вернул статус {response.status_code} для термина "{term}"')
            return None
    except Exception as e:
        logger.error(f'Ошибка при получении термина из Wikipedia: {e}')
        return None

async def search_wikipedia(term: str, language: str = 'en') -> str:
    try:
        url = f'https://{language}.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': term,
            'format': 'json'
        }
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            search_results = data.get('query', {}).get('search', [])
            if search_results:
                first_result_title = search_results[0]['title']
                return await fetch_from_wikipedia(first_result_title, language)
            else:
                return None
        else:
            logger.error(f'Wikipedia search API вернул статус {response.status_code} для термина "{term}"')
            return None
    except Exception as e:
        logger.error(f'Ошибка при поиске термина на Wikipedia: {e}')
        return None

async def fetch_from_wiktionary(term: str, language: str = 'en') -> str:
    try:
        term_encoded = quote(term)
        url = f'https://{language}.wiktionary.org/api/rest_v1/page/definition/{term_encoded}'
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(url)
        
        if response.status_code == 200:
            data = response.json()
            for definitions in data.values():
                for entry in definitions:
                    if 'definitions' in entry and entry['definitions']:
                        return entry['definitions'][0]['definition']
            return None
        else:
            logger.error(f'Wiktionary API вернул статус {response.status_code} для термина "{term}"')
            return None
    except Exception as e:
        logger.error(f'Ошибка при получении термина из Wiktionary: {e}')
        return None

async def fetch_from_duckduckgo(term: str, language: str = 'en') -> str:
    try:
        params = {
            'q': term,
            'format': 'json',
            't': 'telegram_bot',
            'ia': 'meanings',
            'kl': f'{language}-{language.upper()}',
        }
        url = 'https://api.duckduckgo.com/'
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            abstract = data.get('AbstractText')
            if abstract:
                return abstract
            elif data.get('RelatedTopics'):
                for topic in data['RelatedTopics']:
                    if 'Text' in topic:
                        return topic['Text']
            return None
        else:
            logger.error(f'DuckDuckGo API вернул статус {response.status_code} для термина "{term}"')
            return None
    except Exception as e:
        logger.error(f'Ошибка при получении термина из DuckDuckGo: {e}')
        return None

async def fetch_from_other_sources(term: str, language: str = 'en') -> str:
    definition = await fetch_from_wikipedia(term, language)
    if definition:
        return definition

    definition = await fetch_from_wiktionary(term, language)
    if definition:
        return definition

    definition = await fetch_from_duckduckgo(term, language)
    if definition:
        return definition
    
    # pre-release - not full paths
    return None
