import logging
from ml.utils import preprocess_term, vectorize_terms
from ml.classifier import classify_term_context
from ml.generate_definition import generate_definition
from ml.recommendation import recommend_terms
from ml.notification_bot import send_message
from ml.analysis import analyze_term_searches, visualize_recommendations
import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def train_and_notify(term, definition):
    logging.info(f"Начинается обработка термина '{term}'")

    # 1. Предобработка термина
    processed_term = preprocess_term(term)
    logging.info(f"Предобработанный термин: {processed_term}")

    # 2. Векторизация терминов (простой пример, можно улучшить)
    terms = [processed_term]
    term_vectors = vectorize_terms(terms)
    logging.info(f"Векторизация завершена для термина: {processed_term}")

    # 3. Классификация термина
    try:
        context = classify_term_context(processed_term, definition)
        logging.info(f"Контекст для термина '{term}' определен как: {context}")
    except Exception as e:
        logging.error(f"Ошибка при классификации термина '{term}': {e}")
        send_message(f"Ошибка классификации термина '{term}': {e}")
        return

    # 4. Генерация определения
    try:
        generated_definition = generate_definition(term)
        logging.info(f"Сгенерированное определение для термина '{term}': {generated_definition}")
    except Exception as e:
        logging.error(f"Ошибка при генерации определения для термина '{term}': {e}")
        send_message(f"Ошибка генерации определения для термина '{term}': {e}")
        return

    # 5. Рекомендация похожих терминов
    user_history = term_vectors  # Пример использования вектора термина как истории
    recommended_terms = recommend_terms(user_history, term_vectors)
    logging.info(f"Рекомендованные термины для '{term}': {recommended_terms}")

    # 6. Анализ и визуализация
    df = pd.DataFrame({'term': terms, 'vector': term_vectors})
    analyze_term_searches(df)
    df_recommendations = pd.DataFrame({'term': terms, 'score': [1.0]})
    visualize_recommendations(df_recommendations)

    # 7. Отправка отчета в бота
    report = (f"Термин: {term}\n"
              f"Предсказанный контекст: {context}\n"
              f"Сгенерированное определение: {generated_definition}\n"
              f"Рекомендованные термины: {recommended_terms}")
    
    try:
        send_message(report)
        logging.info(f"Отчет успешно отправлен для термина '{term}'")
    except Exception as e:
        logging.error(f"Ошибка при отправке отчета для термина '{term}': {e}")
 