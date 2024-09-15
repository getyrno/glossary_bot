# ml/utils.py
import numpy as np

def preprocess_term(term):
    return term.lower().strip()

def vectorize_terms(terms):
    return np.array([hash(term) % 1000 for term in terms])
