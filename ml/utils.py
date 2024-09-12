# ml/utils.py
import numpy as np

def preprocess_term(term):
    """
    Предобработка термина перед классификацией или генерацией.
    """
    return term.lower().strip()

def vectorize_terms(terms):
    """
    Преобразует список терминов в числовые векторы.
    """
    return np.array([hash(term) % 1000 for term in terms])  # Пример простой векторизации
