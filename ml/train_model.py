import logging
from ml.utils import preprocess_term, vectorize_terms
from ml.classifier import classify_term_context
from ml.generate_definition import generate_definition_gpt2
from ml.notification_bot import send_message
from ml.analysis import analyze_term_searches, visualize_recommendations
import pandas as pd

logging.basicConfig(level=logging.INFO)

def train_and_notify(term, definition):
    logging.info(f"Начинается обработка термина '{term}'")

    processed_term = preprocess_term(term)
    logging.info(f"Предобработанный термин: {processed_term}")

    terms = [processed_term]
    term_vectors = vectorize_terms(terms)
    logging.info(f"Векторизация завершена для термина: {processed_term}")

    try:
        context = classify_term_context(processed_term, definition)
        logging.info(f"Контекст для термина '{term}' определен как: {context}")
    except Exception as e:
        logging.error(f"Ошибка при классификации термина '{term}': {e}")
        send_message(f"Ошибка классификации термина '{term}': {e}")
        return

    # 4. Генерация определения
    # try:
    #     generated_definition = generate_definition_gpt2(term)
    #     logging.info(f"Сгенерированное определение для термина '{term}': {generated_definition}")
    # except Exception as e:
    #     logging.error(f"Ошибка при генерации определения для термина '{term}': {e}")
    #     send_message(f"Ошибка генерации определения для термина '{term}': {e}")
    #     return

    # 5. Рекомендация похожих терминов
    # user_history = term_vectors  # Пример использования вектора термина как истории
    # recommended_terms = recommend_terms(user_history, term_vectors)
    # logging.info(f"Рекомендованные термины для '{term}': {recommended_terms}")

    report = (f"Термин: {term}\n"
              f"Предсказанный контекст: {context}\n"
              f"Сгенерированное определение: В разработке")
    
    try:
        send_message(report)
        logging.info(f"Отчет успешно отправлен для термина '{term}'")
    except Exception as e:
        logging.error(f"Ошибка при отправке отчета для термина '{term}': {e}")
  