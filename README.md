# Zepto Data & AI Platform

A complete data engineering, analytics, and AI-powered customer-support platform inspired by Zepto.

## Modules

### Module 1: Data Engineering

- Extracts and processes book data
- Uses SQLite for storage
- Implements a basic ETL pipeline

### Module 2: Data Analytics

- Titanic dataset analysis
- Data cleaning and preprocessing
- Exploratory Data Analysis
- Machine learning pipeline
- Saved cleaned dataset and model

### Module 3: AI Support Assistant Backend

- Retrieval-Augmented Generation architecture
- Local embeddings using `all-MiniLM-L6-v2`
- ChromaDB vector database
- LangGraph workflow
- Intent classification
- Source-aware responses
- FastAPI `/ask` endpoint

### Module 4: Streamlit Frontend

- User-friendly support assistant interface
- Sends questions to the FastAPI backend
- Displays answers, sources, and confidence score

## Project Structure

```text
zepto-data-ai-platform/
├── data_pipeline/
├── analytics/
├── support_assistant/
│   ├── docs/
│   ├── chroma_db/
│   ├── ingest.py
│   ├── main.py
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── .gitignore
└── README.md