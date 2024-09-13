import logging
import asyncio
import os
import time
from deep_translator import GoogleTranslator
from transformers import pipeline
from functools import lru_cache
import psutil  # Для мониторинга загрузки CPU

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levellevel)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

# Модель классификации
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Переводчик
translator = GoogleTranslator(source='auto', target='en')

# Кэширование результатов
@lru_cache(maxsize=1000)  # Кэшируем до 1000 последних запросов
def classify_term_context(term, definition):
    logger.info("Начало функции классификации")

    candidate_labels = [
        "математика", "физика", "химия", "биология", "геология", "астрономия",
    "науки о Земле", "экология", "оценка воздействия на окружающую среду",
    
    # Технические науки
    "инженерия", "электротехника", "механика", "робототехника", "материаловедение", 
    "нанотехнологии", "оптика", "криптография", "энергетика", "ядерная физика",
    "авиационная техника", "космическая техника", "информационная безопасность",
    
    # Компьютерные науки и IT
    "программирование", "информатика", "веб-разработка", "облачные вычисления",
    "разработка игр", "искусственный интеллект", "машинное обучение", "наука о данных",
    "квантовые вычисления", "блокчейн", "алгоритмы", "базы данных",
    "интернет вещей", "кибербезопасность", "разработка мобильных приложений",
    
    # Социальные науки и гуманитарные дисциплины
    "социология", "психология", "философия", "политология", "экономика",
    "литература", "история", "лингвистика", "культурология", "педагогика", 
    "искусствоведение", "археология", "антропология", "религиоведение", 
    
    # Прикладные науки
    "медицина", "фармацевтика", "ветеринария", "здравоохранение", 
    "химическая инженерия", "строительство", "архитектура", "логистика", 
    "градостроительство", "пищевые технологии", "сельское хозяйство", "агрономия", 
    
    # Искусство и творчество
    "музыка", "живопись", "театральное искусство", "кинематограф", 
    "мода", "фотография", "дизайн", "графический дизайн", "анимация"
]

    logger.info(f"Термин: {term}, Определение: {definition}")
    text = f"Термин: {term}. Определение: {definition}"
    logger.info("Вызов модели для классификации")
    
    result = classifier(text, candidate_labels)
    all_metrics = list(zip(result['labels'], result['scores']))
    
    logger.info("Результаты классификации:")
    for label, score in all_metrics:
        logger.info(f"Метка: {label}, Вероятность: {score:.4f}")
    
    best_label = result['labels'][0]
    best_score = result['scores'][0]
    
    logger.info("Конец функции классификации")
    return f"{best_label}: {best_score:.4f}"

# Асинхронный вызов для интеграции с другими функциями
async def classify_term_context_async(term, definition):
    # Получаем текущую загрузку CPU
    cpu_load = psutil.cpu_percent(interval=1)
    logger.info(f"Текущая загрузка CPU: {cpu_load}%")
    
    # Проверяем, если загрузка CPU ниже 20%, выполняем задачу
    if cpu_load < 20:
        logger.info("Загрузка CPU низкая, выполняем задачу")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, classify_term_context, term, definition)
        return result
    else:
        # Если CPU выше 20%, сохраняем задачу в кэш для выполнения позднее
        logger.info(f"Загрузка CPU {cpu_load}%, сохраняем задачу в кэш")
        return await cache_task(term, definition)

# Функция для кэширования задач
@lru_cache(maxsize=1000)
async def cache_task(term, definition):
    logger.info(f"Сохраняем в кэш: {term}")
    return f"Задача для термина '{term}' сохранена в кэш. Выполнится позже."
