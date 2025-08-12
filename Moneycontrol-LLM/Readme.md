# Moneycontrol News Query System

## 📌 Overview
This project automates the process of fetching financial news from **[Moneycontrol](https://www.moneycontrol.com/news/)**, storing it in a **PostgreSQL** database, and allowing users to query the news using **natural language** with **Google Gemini** via **LangChain**.

The workflow:
1. **Scraping** – Collects news articles from all Moneycontrol categories.
2. **Storage** – Saves articles in PostgreSQL using SQLAlchemy.
3. **Processing** – Splits news text into chunks and generates vector embeddings with Google Generative AI.
4. **Querying** – Uses FAISS vector search + Gemini LLM to answer user questions about stored news.

---

## 🛠 Tech Stack
- **Python** – Core programming language
- **PostgreSQL** – Database for storing articles
- **SQLAlchemy** – ORM for database operations
- **Requests & BeautifulSoup** – Web scraping
- **LangChain** – Text processing, vector storage, and QA pipeline
- **FAISS** – Vector similarity search
- **Google Gemini API** – Natural language processing

---

## 📂 Project Structure

project/
│
├── stocks/   
│ ├── database_management.py # Handles DB CRUD operations   
│ 
├── fetch_data.py # Scrapes and stores articles   
├── para_processing.py # Splits, embeds, and queries articles   
├── requirements.txt # Python dependencies   
├── README.md # Project documentation   

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/moneycontrol-news-query.git
cd moneycontrol-news-query
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Environment Variables
Create a .env file or set environment variables in your shell:
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/Gold"
export GOOGLE_API_KEY="your_google_api_key_here"
```

### 4️⃣ Setup PostgreSQL Database
Ensure you have a table named news_articles:
```bash
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    cont TEXT
);
```

### 5️⃣ Fetch News Data
```bash
python fetch_data.py
```
This will scrape Moneycontrol news and store it in your PostgreSQL database.

### 6️⃣ Query the News
```bash
python para_processing.py
```
Enter a keyword to filter articles from the database.
Enter your natural language question to get an AI-generated answer.

### 🚀 Future Improvements
Save FAISS index to disk for faster querying.

Add scheduled scraping (daily updates via cron or APScheduler).

Build a simple FastAPI/Streamlit UI for interactive querying.
