import logging
from deep_translator import GoogleTranslator
from transformers import pipeline

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

translator = GoogleTranslator(source='auto', target='en')

def classify_term_context(term, definition):
    logger.debug("Начало функции классификации")
    
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

    
    logger.debug(f"Термин: {term}, Определение: {definition}")
    text = f"Термин: {term}. Определение: {definition}"
    logger.debug("Вызов модели для классификации")
    result = classifier(text, candidate_labels)
    all_metrics = list(zip(result['labels'], result['scores']))
    
    logger.info("Результаты классификации:")
    for label, score in all_metrics:
        logger.info(f"Метка: {label}, Вероятность: {score:.4f}")
    
    best_label = result['labels'][0]
    best_score = result['scores'][0]
    
    logger.debug("Конец функции классификации")
    
    return f"{best_label}: {best_score:.4f}"

