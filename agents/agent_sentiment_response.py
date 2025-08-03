import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATA_FILE = "data/reviews.csv"

def run_sentiment_plot_agent():
    if not os.path.exists(DATA_FILE):
        print("❌ No feedback data found! Add some reviews first.")
        return

    df = pd.read_csv(DATA_FILE, parse_dates=["timestamp"])

    start_date = input("📅 Enter start date (YYYY-MM-DD): ")
    end_date = input("📅 Enter end date (YYYY-MM-DD): ")

    df_filtered = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]

    if df_filtered.empty:
        print("❌ No data in the selected range.")
        return

    df_grouped = df_filtered.groupby([df_filtered["timestamp"].dt.date, "sentiment"]).size().unstack(fill_value=0)

    plt.figure(figsize=(8, 5))
    df_grouped.plot(kind="bar", stacked=True, colormap="coolwarm", figsize=(10, 6))
    plt.title("Sentiment Trend")
    plt.xlabel("Date")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
