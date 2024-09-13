import logging
from deep_translator import GoogleTranslator
from transformers import pipeline

# Настройка отдельного логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Создаем формат для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(console_handler)

# Инициализация модели классификации
classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

# Инициализация переводчика
translator = GoogleTranslator(source='auto', target='en')

def classify_term_context(term, definition):
    logger.debug("Начало функции классификации")
    
    # Расширенные контексты для классификации
    candidate_labels = [
        "математика", "программирование", "биология", "экономика", "физика",
        "химия", "психология", "философия", "искусственный интеллект",
        "машинное обучение", "история", "география", "литература", "медицина",
        "социология", "политология", "информатика", "инженерия",
        "нейронаука", "робототехника", "наука о данных", "криптография",
        "веб-разработка", "облачные вычисления", "разработка игр", "экология"
    ]
    
    logger.debug(f"Термин: {term}, Определение: {definition}")
    
    # Классификация с переведенным текстом
    text = f"Термин: {term}. Определение: {definition}"
    
    logger.debug("Вызов модели для классификации")
    result = classifier(text, candidate_labels)
    
    all_metrics = list(zip(result['labels'], result['scores']))
    
    # Логирование всех метрик
    logger.info("Результаты классификации:")
    for label, score in all_metrics:
        logger.info(f"Метка: {label}, Вероятность: {score:.4f}")
    
    best_label = result['labels'][0]
    best_score = result['scores'][0]
    
    logger.debug("Конец функции классификации")
    
    # Возвращаем метку и вероятность
    return f"{best_label}: {best_score:.4f}"

