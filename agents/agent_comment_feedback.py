import os
import pandas as pd
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("❌ GROQ_API_KEY is missing in .env")

llm = ChatGroq(model="llama3-70b-8192", temperature=0.7)

#Prompt Template
prompt = PromptTemplate(
    input_variables=["feedback"],
    template="""
                    You are a polite customer support agent for SteamNoodles.
                    Analyze the following feedback:
                    1️⃣ Identify the sentiment (positive, negative, or neutral).
                    2️⃣ Write a short, polite, and context-aware reply.

                    Return the result in JSON format like this:
                    {"sentiment": "positive/negative/neutral", "reply": "your reply"}

                    Customer feedback: "{feedback}"
                    """
)

chain = LLMChain(llm=llm, prompt=prompt)

DATA_FILE = "data/reviews.csv"

def save_feedback_to_csv(feedback, reply, sentiment):
    df_new = pd.DataFrame([{
        "text": feedback,
        "reply": reply,
        "sentiment": sentiment,
        "timestamp": pd.Timestamp.now()
    }])

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

        response = chain.invoke({"feedback": feedback})["text"]

        try:
            import json
            result = json.loads(response)
            sentiment = result.get("sentiment", "neutral")
            reply = result.get("reply", "Thank you for your feedback!")
        except:
            sentiment = "neutral"
            reply = response

        print(f"\n📣 Agent Reply ({sentiment.upper()}):\n", reply)
        print("-" * 120)

        save_feedback_to_csv(feedback, reply, sentiment)
        print("✅ Feedback, reply & sentiment saved to reviews.csv")
