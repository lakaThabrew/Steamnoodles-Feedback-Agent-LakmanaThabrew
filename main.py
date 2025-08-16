from agents.agent_comment_feedback import run_feedback_agent
from agents.agent_sentiment_response import run_sentiment_plot_agent

while True:
    print("\n")
    print("+-----------------------------------------------------+")
    print("|  🌟 Welcome to the Steam Noodles Feedback System 🌟 |")
    print("+-----------------------------------------------------+")
    print("| 🍜 Steam Noodles Feedback Agents                    |")
    print("|    ------------------------------                   |")
    print("| 1. 📝 Customer Feedback Response Agent              |")
    print("| 2. 📶 Sentiment Visualization Agent                 |")
    print("| 3. 🚪 Exit                                          |")
    print("+-----------------------------------------------------+")

    choice = input("\n🔀 Select an option: ")

    if choice == "1":
        run_feedback_agent()
 
    elif choice == "2":
        run_sentiment_plot_agent()

    elif choice == "3" or "exit" or "Exit" or "quit" or "Quit":
        print("\n👋 Goodbye! Have a great day!")
        break

    else:
        print("\n⚠️ Invalid choice. Enter Valid Input.........................")
