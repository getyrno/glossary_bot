# train_model.py
from ml.classifier import classify_term_context
from ml.notification_bot import send_message

def train_and_notify(term, definition):    
    # Классифицируем контекст термина
    context = classify_term_context(term, definition)
    
    # Отправляем результаты в мониторингового бота
    send_message(f"Term: {term}\nPredicted Context: {context}")
