# # ml/recommendation.py
# import pandas as pd
# from sklearn.neighbors import NearestNeighbors
# from sklearn.feature_extraction.text import TfidfVectorizer

# def vectorize_terms(terms):
#     """
#     Векторизуем термины с использованием TF-IDF.
#     """
#     vectorizer = TfidfVectorizer()
#     return vectorizer.fit_transform(terms).toarray()

# def recommend_terms(user_history, term_vectors, original_terms):
#     """
#     Рекомендуем термины на основе истории пользователя.
#     """
#     # Проверяем форму массива
#     if len(term_vectors.shape) == 1:
#         term_vectors = term_vectors.reshape(-1, 1)
    
#     n_neighbors = min(5, len(term_vectors))  # n_neighbors не должен превышать количество данных

#     model = NearestNeighbors(n_neighbors=n_neighbors)
#     model.fit(term_vectors)

#     if len(user_history.shape) == 1:
#         user_history = user_history.reshape(1, -1)
    
#     distances, indices = model.kneighbors(user_history)
#     recommended_terms = [original_terms[i] for i in indices.flatten()]
    
#     return recommended_terms
