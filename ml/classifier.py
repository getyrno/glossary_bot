import logging
from deep_translator import GoogleTranslator
from transformers import pipeline
from functools import lru_cache
import asyncio
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

translator = GoogleTranslator(source='auto', target='en')
@lru_cache(maxsize=1000)  # Кэшируем до 1000 последних запросов
async def classify_term_context(term, definition):
    logger.info("Начало функции классификации")
    
    candidate_labels = [
    # Естественные науки
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
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, classify_term_context, term, definition)
    return result