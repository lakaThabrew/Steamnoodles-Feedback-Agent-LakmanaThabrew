# 🍜 Automated Restaurant Feedback Agents – SteamNoodles

## 📌 Project Overview

SteamNoodles is a fast-growing restaurant chain known for enhancing customer experience using innovative solutions.
This project builds two AI agents using LangChain to automate customer feedback analysis and response.

## 🎯 Objective
### ✅ Agent 1 – Feedback & Sentiment Response Agents

- Accepts a customer review as input
- Uses an LLM to analyze sentiment (Positive / Negative / Neutral)
- Generates a short, polite, and context-aware automated reply

### ✅ Agent 2 – Sentiment Visualization Agent

- Takes a date range as input (e.g., "last 7 days" or "June 1 to June 15")
- Generates a bar or line plot showing daily sentiment distribution
- Provides dynamic results based on the dataset and user input

## 🛠️ Tools & Technologies
- Frameworks: LangChain
- LLMs: HuggingFace Transformers
- Python Libraries: pandas, matplotlib, seaborn, plotly
- Dataset: Kaggle restaurant reviews dataset (text, sentiment, timestamps
- Platform: Python Script

## 📂 Project Structure
```
steamnoodles-feedback-agent/
  |-- venv
  │-- agents/
  │   ├── agent_comment_feedback.py
  │   ├── agent_sentiment_response.py
  │-- data/
  │   ├── reviews.csv
  │-- outputs/
  │   ├── sample_plots
  │   ├── response.txt
  |-- main.py
  │-- README.md
  │-- requirements.txt
  │-- examples.txt
  |-- .env
  |-- .gitignore
```

## ⚡ Setup Instructions
### 🔹 1️⃣ Clone Repository
```
git clone https://github.com/lakaThabrew/steamnoodles-feedback-agent.git
cd steamnoodles-feedback-agent
```
### 🔹 2️⃣ Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
```
### 🔹 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
### 🔹 4️⃣ Set Up API Keys
Create a .env file and add:
```
OPENAI_API_KEY=your_api_key_here
```

## 🚀 How to Run
### ✅ Run main.py
```
python main.py
```
- 📌 Enter a customer review, and the agent will detect sentiment & generate a reply.
-  📌 Enter a date range (e.g., "last 7 days"). The agent will generate a sentiment plot.

## 📊 Sample Outputs
### 🔹 Feedback Response Agent
```
Input: "The noodles were delicious, and the delivery was so fast!"
Output: "Thank you so much for sharing your wonderful experience!
         We're thrilled that you enjoyed our noodles and quick delivery.
         We can’t wait to serve you again soon!"
```

### 🔹 Sentiment Visualization Agent
```
📈 Example Plot:
```

## 🧑‍💻 Author
Name: Lakmana Thabrew

University: 
```
Department of Computer Science & Engineering,
Faculty of Engineering,
University of Moratuwa,
Sri Lanka.
```

Year: 23 Batch, Second Year

## 📜 License
This project is licensed under the MIT License.

## 📞 Contact for Support
🧑‍💻 Lakmana Thabrew

📧 Email : 
```
lakmanat.23@cse.mrt.ac.lk
```
