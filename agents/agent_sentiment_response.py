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
    raise EnvironmentError("\n⚠️ GROQ_API_KEY is missing in .env")

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

    user_input = input("\n📅 Enter date range (e.g., 'last 7 days', 'June 1 to June 15'): ")

    start_date, end_date = get_date_range(user_input)

    if not start_date or not end_date:
        print("\n⚠️ Could not understand the date range. Try again.")
        return

    df_filtered = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]

    if df_filtered.empty:
        print("\n⚠️ No data available in the selected range.")
        return

    df_grouped = (df_filtered.groupby([df_filtered["timestamp"].dt.date, "sentiment"]).size().unstack(fill_value=0))

    ordered_sentiments = ['positive', 'neutral', 'negative']
    df_grouped = df_grouped.reindex(columns=ordered_sentiments, fill_value=0)

    fig, ax1 = plt.subplots(figsize=(12, 7))
    line_colors = {'positive': '#2E8B57', 'neutral': '#DAA520', 'negative': '#DC143C'}  
    line_markers = {'positive': 'o', 'neutral': 'o', 'negative': 'o'}  
    
    df_grouped[ordered_sentiments].plot(kind="bar",stacked=False,color=line_colors,edgecolor='black',ax=ax1,alpha=0.8,linewidth=0.5)

    ax2 = ax1.twinx()

    for sentiment in ordered_sentiments:
        ax2.plot(range(len(df_grouped)), df_grouped[sentiment],color=line_colors[sentiment], 
                marker=line_markers[sentiment], linewidth=2.5, markersize=6, label=f"{sentiment.title()} Trend",
                markerfacecolor='white', markeredgecolor=line_colors[sentiment], markeredgewidth=2)

    ax1.set_title(f"Sentiment Trend Analysis ({start_date.date()} → {end_date.date()})",fontsize=16, weight='bold')
    ax1.set_xlabel("Date", fontsize=12)
    ax1.set_ylabel("Number of Reviews (Stacked)", fontsize=12)
    ax2.set_ylabel("Individual Sentiment Count (Lines)", fontsize=12)
    ax1.set_xticks(range(len(df_grouped)))
    ax1.set_xticklabels([str(date) for date in df_grouped.index], rotation=45)
    ax1.legend(title="Bars", loc="upper left")
    ax2.legend(title="Trend Lines", loc="upper right")
    ax1.grid(True, axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()

    test_no = int(input("Enter the test Number: "))
    filename = "test#" + str(test_no) + ".png"
    plt.savefig("Outputs/sample_plots/" + filename, dpi=300)
    print(f"\n📊 Sentiment trend plot saved as {filename}.")

    plt.show()

"""
#for checking agent
if __name__ == "__main__":
    while True:
        user = user_input = input("Enter date range (e.g., 'last 7 days', 'June 1 to June 15'): ")
        if user.lower() in ["exit", "quit"]:
            print("Bye")
        run_sentiment_plot_agent()
"""