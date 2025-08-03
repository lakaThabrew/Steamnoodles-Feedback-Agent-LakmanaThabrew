import os
from dotenv import load_dotenv

from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.chat_models.base import BaseChatModel
import pandas as pd

# Load .env file and GROQ key
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise EnvironmentError("GROQ_API_KEY is missing. Please check your .env file.")
else:
    print("GROQ key loaded.")
    
os.environ["GROQ_API_KEY"] = groq_key

llm = ChatGroq(model="llama3-70b-8192", temperature=0.7)

DATA_FILE = "data/reviews.csv"

#Agent 1: Sentiment Analyzer
def sentiment_agent(feedback: str) -> str:
    prompt = f"""
            You are a helpful assistant.
            Given the customer feedback below, determine the sentiment.
            Output ONLY one word: positive, negative, or neutral.

            Customer feedback:
            \"\"\"{feedback}\"\"\"
            """
    
    if isinstance(llm, BaseChatModel):
        response = llm([HumanMessage(content=prompt)])
        return response.content.strip().lower()
    else:
        return llm(prompt).strip().lower()

sentiment_tool = Tool(
    name="SentimentAgent",
    func=sentiment_agent,
    description="Determines just sentiment (positive, negative, neutral) from customer feedback."
)

sentiment_agent_chain = initialize_agent(
    tools=[sentiment_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

#Agent 2: Reply Generator
def reply_agent(feedback: str) -> str:
    prompt = f"""
                You are a polite customer support agent for SteamNoodles.
                Read the customer feedback below and write a short, polite, and context-aware just reply as a paragraph.
                Customer feedback:
                    \"\"\"{feedback}\"\"\"
                """
    
    if isinstance(llm, BaseChatModel):
        response = llm([HumanMessage(content=prompt)])
        return response.content.strip()
    else:
        return llm(prompt).strip()

reply_tool = Tool(
    name="ReplyAgent",
    func=reply_agent,
    description="Generates a polite, context-aware reply to customer feedback as a paragraph."
)

reply_agent_chain = initialize_agent(
    tools=[reply_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

def save_feedback_to_csv(feedback, reply, sentiment):
    df_new = pd.DataFrame([{
        "text": feedback,
        "reply": reply,
        "sentiment": sentiment,
        "timestamp\n\n": pd.Timestamp.now()
    }])

    os.makedirs("data", exist_ok=True)

    if os.path.exists(DATA_FILE):
        df_new.to_csv(DATA_FILE, mode="a", index=False, header=False)

    else:
        df_new.to_csv(DATA_FILE, index=False)

def run_feedback_agent():
    print("SteamNoodles Feedback Sentiment and Reply Agents")
    while True:
        feedback = input("\nEnter customer feedback (type 'exit' to quit): ")

        if feedback.lower() in ["exit", "quit"]:
            print("Back To Main Menu.")
            break

        sentiment_raw = sentiment_agent_chain.invoke(f"Analyze sentiment of this feedback:\n'{feedback}'")
        sentiment_full = sentiment_raw['output'].strip().lower()

        if "positive" in sentiment_full:
            sentiment = "positive"

        elif "negative" in sentiment_full:
            sentiment = "negative"

        elif "neutral" in sentiment_full:
            sentiment = "neutral"

        else:
            sentiment = "unknown"

        reply_raw = reply_agent_chain.invoke(f"Generate a polite reply to this feedback:\n'{feedback}'")
        reply = reply_raw['output'].strip()

        with open("Outputs/response.txt", "a") as f:
            f.write(f"Feedback: {feedback}\n")
            f.write(f"Reply: {reply}\n")
            f.write(f"Sentiment: {sentiment}\n\n")

        save_feedback_to_csv(feedback, reply, sentiment)

        print(f"\nSentiment → {sentiment.capitalize()}")
        print(f"Reply → {reply}")
        print("-" * 170)

#if __name__ == "__main__":
#    run_feedback_agent()