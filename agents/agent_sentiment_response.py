import pandas as pd
import matplotlib.pyplot as plt
import os
import json, re
from datetime import datetime
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("GROQ_API_KEY is missing in .env")

llm = ChatGroq(model="llama3-70b-8192")

DATA_FILE = "data/reviews.csv"

def get_date_range(user_input: str):
    prompt = PromptTemplate(
        template="""
                    You are a date range parser. 
                    Given a user query like "{query}", return a JSON with exact start_date and end_date in YYYY-MM-DD format.
                    Today is {today}.
                    Example outputs:
                    {{"start_date": "2025-07-01", "end_date": "2025-07-15"}}

                    User Query: {query}
                """,
        input_variables=["query", "today"]
    )

    response = llm.predict(prompt.format(query=user_input, today=datetime.today().date()))
    #print(f"AI Response: {response}")

    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group())
            return pd.to_datetime(data["start_date"]), pd.to_datetime(data["end_date"])
        except:
            return None, None
    return None, None

def run_sentiment_plot_agent():
    if not os.path.exists(DATA_FILE):
        print("File Not Found.")
        return

    df = pd.read_csv(
        DATA_FILE,
        header=None,
        names=["review", "response", "sentiment", "timestamp"],
        parse_dates=["timestamp"]
    ).dropna(subset=["timestamp"])

    user_input = input("Enter date range (e.g., 'last 7 days', 'June 1 to June 15'): ")

    start_date, end_date = get_date_range(user_input)

    if not start_date or not end_date:
        print("Could not understand the date range. Try again.")
        return

    df_filtered = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]

    if df_filtered.empty:
        print("No data available in the selected range.")
        return

    df_grouped = (
        df_filtered.groupby([df_filtered["timestamp"].dt.date, "sentiment"])
        .size()
        .unstack(fill_value=0)
    )

    ax = df_grouped.plot(kind="bar", stacked=True, colormap="coolwarm", figsize=(10, 6))
    ax.set_title(f"Sentiment Trend ({start_date.date()} → {end_date.date()})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Reviews")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

""""
if __name__ == "__main__":
    while True:
        user = user_input = input("Enter date range (e.g., 'last 7 days', 'June 1 to June 15'): ")
        if user.lower() in ["exit", "quit"]:
            print("Bye")
        values = get_date_range_from_ai(user)
        print(values)
"""