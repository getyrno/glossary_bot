# ml/analysis.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_term_searches(df):
    sns.countplot(x='term', data=df)
    plt.title("Term Search Frequency")
    plt.show()

def visualize_recommendations(df):
    sns.barplot(x='term', y='score', data=df)
    plt.title("Recommended Terms")
    plt.show()
