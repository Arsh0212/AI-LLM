# 💬 SQL-LangChain Query Assistant

A powerful Streamlit-based natural language interface to query your SQL database using [Google Gemini LLM](https://ai.google), powered by [LangChain](https://www.langchain.com/) and `mysql-connector`.

---
![Mermaid x SQL](https://github.com/user-attachments/assets/c027b6df-0780-49b9-9e94-8637439470a2)




## 🚀 Features

- 🧠 Ask questions in plain English.
- 🗃️ Automatically generates SQL queries from your question.
- ⚙️ Executes the query on your local MySQL database.
- 📊 Displays clean, tabular results using Streamlit.
- 🔐 Gemini (via Google Generative AI) for LLM-based SQL generation.
- 🔄 Supports schema reflection for real-time query adaptation.

---

## 📦 Tech Stack

| Tool        | Role                          |
|-------------|-------------------------------|
| Python      | Core language                  |
| Streamlit   | Web UI                         |
| LangChain   | Prompt chaining & parsing      |
| Gemini API  | LLM for generating SQL         |
| SQLAlchemy  | Database reflection & execution|
| MySQL       | Underlying database            |

---

## 🏗️ Project Structure
📁 SQL-LLM/  
├── main.py # Streamlit app logic  
├── requirements.txt # Python dependencies  
├── README.md # This file  

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Arsh0212/AI-LLM/SQL-LLM.git
cd SQL-LLM
```

### 2. Install dependencies
Make sure you’re using Python 3.9+ and run:

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app

```bash
streamlit run main.py
```
