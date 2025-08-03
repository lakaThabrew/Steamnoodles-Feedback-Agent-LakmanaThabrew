import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

DATA_FILE = "data/reviews.csv"

def run_sentiment_plot_agent():
    if not os.path.exists(DATA_FILE):
        print("❌ No feedback data found.")
        return

    df = pd.read_csv(DATA_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    start = input("Enter start date (YYYY-MM-DD): ")
    end = input("Enter end date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        print("❌ Invalid date format.")
        return

    filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    if filtered.empty:
        print("❌ No reviews in this range.")
        return

    sentiment_counts = filtered.groupby(["date", "sentiment"]).size().unstack(fill_value=0)

    plt.figure(figsize=(10, 6))
    sentiment_counts.plot(kind="bar")
    plt.title(f"Sentiment Trends ({start_date} to {end_date})")
    plt.xlabel("Date")
    plt.ylabel("Number of Reviews")
    plt.legend(title="Sentiment")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("sentiment_plot.png")
    plt.show()

    print("✅ Sentiment plot saved as sentiment_plot.png")
