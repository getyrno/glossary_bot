# # ml/recommendation.py
# import pandas as pd
# from sklearn.neighbors import NearestNeighbors

# def recommend_terms(user_history, term_vectors):
#     # Обучаем модель K-ближайших соседей для поиска похожих терминов
#     model = NearestNeighbors(n_neighbors=5)
#     model.fit(term_vectors)
    
#     # Рекомендуем похожие термины на основе истории пользователя
#     distances, indices = model.kneighbors(user_history)
#     recommended_terms = [term_vectors[i] for i in indices.flatten()]
    
#     return recommended_terms
