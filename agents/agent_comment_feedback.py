import os
import pandas as pd
import json
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

# ✅ Load API Key
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("❌ GROQ_API_KEY is missing in .env")

llm = ChatGroq(model="llama3-70b-8192", temperature=0.7)

prompt = PromptTemplate(
    input_variables=["feedback"],
    template=
            """
                You are a polite customer support agent for SteamNoodles.

                Analyze the following customer feedback and determine its sentiment:
                - Sentiment must be strictly one of: "positive", "negative", or "neutral".
                - Then, write a short, polite, and context-aware reply.

                ⚠️ IMPORTANT: Reply ONLY in valid JSON. Do NOT add extra text.

                Example Output:
                {"sentiment": "positive", "reply": "Thank you so much for your kind words! We're thrilled you enjoyed our noodles."}

                Customer feedback: "{feedback}"
            """
)

chain = prompt | llm  

DATA_FILE = "data/reviews.csv"


def save_feedback_to_csv(feedback, reply, sentiment):
    df_new = pd.DataFrame([{
        "text": feedback,
        "reply": reply,
        "sentiment": sentiment,
        "timestamp": pd.Timestamp.now()
    }])

    os.makedirs("data", exist_ok=True)

    if os.path.exists(DATA_FILE):
        df_new.to_csv(DATA_FILE, mode="a", index=False, header=False)
    else:
        df_new.to_csv(DATA_FILE, index=False)


def run_feedback_agent():
    while True:
        feedback = input("\n💬 Enter customer feedback (type 'exit' to quit): ")
        if feedback.lower() in ["exit", "quit"]:
            print("👋 Exiting Feedback Agent.\n")
            break

        result = chain.invoke({"feedback": feedback}) 

        raw_text = result.content if hasattr(result, "content") else str(result)

        try:
            parsed = json.loads(raw_text)
            sentiment = parsed.get("sentiment", "neutral")
            reply = parsed.get("reply", "Thank you for your feedback!")
        except:
            sentiment = "neutral"
            reply = raw_text.strip()

        print(f"\n📣 Sentiment → {sentiment.upper()}")
        print(f"💬 Reply → {reply}")
        print("-" * 100)

        save_feedback_to_csv(feedback, reply, sentiment)
        print("✅ Saved to reviews.csv")


