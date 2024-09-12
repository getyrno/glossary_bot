# ml/analysis.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_term_searches(df):
    """
    Визуализирует частоту запросов терминов.
    
    df: DataFrame с данными о поисках терминов.
    """
    sns.countplot(x='term', data=df)
    plt.title("Term Search Frequency")
    plt.show()

def visualize_recommendations(df):
    """
    Визуализирует рекомендованные термины.
    
    df: DataFrame с данными о рекомендациях.
    """
    sns.barplot(x='term', y='score', data=df)
    plt.title("Recommended Terms")
    plt.show()
