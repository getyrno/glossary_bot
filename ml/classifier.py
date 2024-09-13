from deep_translator import GoogleTranslator
from transformers import pipeline
import logging

# Инициализация модели классификации
classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

# Инициализация переводчика
translator = GoogleTranslator(source='auto', target='en')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Убедитесь, что логи выводятся в консоль
)

def classify_term_context(term, definition):
    logging.debug("Начало функции классификации")

    # Расширенные контексты для классификации
    candidate_labels = [
    "математика", "программирование", "биология", "экономика", "физика",
    "химия", "психология", "философия", "искусственный интеллект",
    "машинное обучение", "история", "география", "литература", "медицина",
    "социология", "политология", "информатика", "инженерия",
    "нейронаука", "робототехника", "наука о данных", "криптография",
    "веб-разработка", "облачные вычисления", "разработка игр", "экология"
]

    
    # Классификация с переведенным текстом
    text = f"Термин: {term}. Определение: {definition}"
    
    result = classifier(text, candidate_labels)
    all_metrics = list(zip(result['labels'], result['scores']))
    
    # Печатаем все метрики
    logging.info("Результаты классификации:")
    for label, score in all_metrics:
        logging.info(f"Метка: {label}, Вероятность: {score:.4f}")
    best_label = result['labels'][0]
    best_score = result['scores'][0]
    
    # Возвращаем метку и вероятность
    return f"{best_label}: {best_score:.4f}"
