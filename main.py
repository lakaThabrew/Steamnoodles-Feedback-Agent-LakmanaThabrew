from agents.agent_comment_feedback import run_feedback_agent
from agents.agent_sentiment_response import run_sentiment_plot_agent

while True:
    print("\n🚀 Steam Noodles Feedback Agents")
    print("1️⃣ Customer Feedback Response Agent")
    print("2️⃣ Sentiment Visualization Agent")
    print("3️⃣ Exit")

    choice = input("👉 Select an option: ")

    if choice == "1":
        run_feedback_agent()

    elif choice == "2":
        run_sentiment_plot_agent()

    elif choice == "3":
        print("👋 Goodbye!")
        break

    else:
        print("❌ Invalid choice. Enter Valid Input.........................")

