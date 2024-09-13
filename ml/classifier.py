from deep_translator import GoogleTranslator
from transformers import pipeline

# Инициализация модели классификации
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# result = classifier("Test term", candidate_labels=["science", "art", "programming"])
# print(result)
# Инициализация переводчика
translator = GoogleTranslator(source='auto', target='en')

def classify_term_context(term, definition):
    """
    Классифицируем контекст термина с переводом на английский язык.
    
    :param term: Сам термин.
    :param definition: Описание или определение термина.
    :return: Предсказанный контекст.
    """
    # Переводим термин и определение на английский язык
    term_en = translator.translate(term)
    definition_en = translator.translate(definition)
    
    # Объединяем переведенный текст для модели
    text = f"Term: {term_en}. Definition: {definition_en}"
    
    # Расширенные контексты для классификации
    candidate_labels = [
        "mathematics", "programming", "biology", "economics", "physics", 
        "chemistry", "psychology", "philosophy", "artificial intelligence", 
        "machine learning", "history", "geography", "literature", "medicine",
        "sociology", "political science", "computer science", "engineering", 
        "neuroscience", "robotics", "data science", "cryptography",
        "web development", "cloud computing", "game development", "environmental science"
    ]
    
    # Классификация с переведенным текстом
    result = classifier(text, candidate_labels)
    
    # Возвращаем контекст с наивысшей вероятностью
    return result['labels'][0]
