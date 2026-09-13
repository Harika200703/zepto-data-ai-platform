# Zepto Data & AI Platform

A complete data engineering, analytics, and AI-powered customer-support platform inspired by Zepto.

## Project Structure

```text
zepto-data-ai-platform/
├── data_pipeline/
│   ├── scraper.py
│   ├── database.py
│   ├── queries.sql
│   └── README.md
├── analytics/
│   ├── titanic_eda.ipynb
│   ├── titanic.csv
│   ├── titanic_clean.csv
│   ├── titanic_final_pipeline.joblib
│   └── README.md
├── support_assistant/
│   ├── docs/
│   ├── ingest.py
│   ├── main.py
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements-docker.txt
│   └── README.md
├── .gitignore
└── README.md
```

## Modules

### Module 1: Data Engineering

This module implements a basic ETL pipeline:

* Extracts book data from an online books source.
* Stores the extracted data in CSV format.
* Loads the data into a SQLite database.
* Creates and uses book categories.
* Executes SQL analysis queries.

**Design decisions:**

* Python is used for extraction and database loading.
* SQLite is used because it is lightweight and does not require a separate database server.
* CSV is used as an intermediate storage format.
* SQL queries are stored separately in `queries.sql` for clarity and reuse.

### Module 2: Data Analytics

This module performs Titanic dataset analysis and machine learning:

* Loads the Titanic dataset.
* Cleans missing and inconsistent values.
* Performs exploratory data analysis.
* Preprocesses numerical and categorical features.
* Trains and evaluates machine learning models.
* Saves the cleaned dataset and final machine learning pipeline.

**Design decisions:**

* Pandas is used for data cleaning and analysis.
* Matplotlib and Seaborn are used for visual analysis.
* Scikit-learn pipelines combine preprocessing and model training.
* The trained pipeline is saved using Joblib so it can be reused without retraining.

### Module 3: AI Customer Support Assistant

This module implements a Retrieval-Augmented Generation-style support assistant:

* Stores support documents in a local ChromaDB vector database.
* Uses the `all-MiniLM-L6-v2` embedding model.
* Retrieves relevant support information.
* Classifies user intent.
* Generates source-aware answers.
* Provides a FastAPI `/ask` endpoint.
* Includes a Streamlit frontend.

**Design decisions:**

* Local embeddings are used to avoid paid external embedding APIs.
* ChromaDB provides persistent vector storage and similarity search.
* FastAPI is used to expose the backend through a simple API.
* Streamlit provides an easy-to-use frontend.
* The system uses local support documents so answers remain grounded in the available information.
* Docker support is included for easier deployment.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Harika200703/zepto-data-ai-platform.git
cd zepto-data-ai-platform
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the required packages for the relevant module.

## How to Run Module 1

```powershell
cd data_pipeline
python scraper.py
python database.py
```

To view the SQL queries:

```powershell
Get-Content queries.sql
```

The module generates the book CSV data and SQLite database.

## How to Run Module 2

Open the notebook:

```text
analytics/titanic_eda.ipynb
```

Run all notebook cells in Jupyter Notebook or VS Code.

The notebook produces:

* `titanic_clean.csv`
* `titanic_final_pipeline.joblib`

## How to Run Module 3

### Install backend dependencies

From the project root:

```powershell
cd support_assistant
pip install -r requirements.txt
```

### Ingest support documents

```powershell
python ingest.py
```

### Start the FastAPI backend

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

```powershell
cd support_assistant
streamlit run app.py
```

The Streamlit interface will open in the browser.

## Docker

From the project root:

```powershell
docker build -t zepto-support-assistant ./support_assistant
docker run -p 7860:7860 zepto-support-assistant
```

Open:

```text
http://localhost:7860/docs
```

## Technologies Used

* Python
* Pandas
* NumPy
* SQLite
* SQL
* Jupyter Notebook
* Scikit-learn
* Matplotlib
* Seaborn
* FastAPI
* Streamlit
* ChromaDB
* LangGraph
* Sentence Transformers
* Docker

## Academic Integrity

This project is developed for educational purposes. The implementation, analysis, and documentation are maintained in this public GitHub repository.
