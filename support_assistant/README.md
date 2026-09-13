# Zepto Support Assistant

A Retrieval-Augmented Generation (RAG) customer-support assistant for Zepto.

## Features

- Uses 8 Zepto support documents as a knowledge base
- Generates embeddings using `all-MiniLM-L6-v2`
- Stores and retrieves documents using ChromaDB
- Uses cosine similarity search with top-3 retrieval
- Uses LangGraph for intent classification and routing
- Provides a FastAPI `/ask` endpoint
- Returns answers, source documents, and confidence scores
- Supports deterministic mock LLM mode by default
- Includes a Streamlit frontend
- Includes Docker support

## Architecture

```text
User Question
      |
      v
FastAPI /ask
      |
      v
LangGraph StateGraph
      |
      v
Intent Classification
      |
      +-----------------------------+
      |                             |
      v                             v
policy_question              general_question
      |                             |
      v                             v
Retrieve Top-3 Documents      Direct Answer
      |
      v
ChromaDB Cosine Similarity Search
      |
      v
Structured Answer
      |
      v
Answer + Sources + Confidence
```

## Project Structure

```text
support_assistant/
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
├── ingest.py
├── main.py
├── app.py
├── Dockerfile
├── requirements.txt
├── requirements-docker.txt
└── chroma_db/
```

## Document Ingestion

The `ingest.py` script:

1. Loads all 8 text documents from the `docs/` directory.
2. Uses each document as a separate text chunk.
3. Generates embeddings with `all-MiniLM-L6-v2`.
4. Stores the embeddings in ChromaDB.
5. Creates the `zepto_support` collection.
6. Stores document IDs as metadata for source tracking.

The ChromaDB collection contains the eight support documents.

Run ingestion locally:

```powershell
python ingest.py
```

## LangGraph Workflow

The assistant uses a LangGraph `StateGraph` with a typed state.

### 1. Intent Classification

The `classify_intent` node classifies the question into one of two labels:

- `policy_question`
- `general_question`

The default mock classifier uses keyword matching for:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

### 2. Retrieve and Answer

The `retrieve_and_answer` node:

- Embeds the user query.
- Performs ChromaDB cosine similarity search.
- Retrieves the top 3 relevant documents.
- Builds a structured prompt.
- Produces a deterministic mock answer by default.
- Returns the retrieved document IDs as sources.
- Returns a confidence score.

### 3. Direct Answer

The `direct_answer` node handles general questions.

In mock mode, it returns:

```text
I can only answer questions about Zepto policies right now.
```

### Conditional Routing

The graph routes the question based on the classified intent:

```text
policy_question  -> retrieve_and_answer
general_question -> direct_answer
```

## Structured Prompt

The prompt contains:

- Role definition
- Retrieved context
- User question
- Task instructions
- Negative constraints
- Output format
- Answer length constraint
- Few-shot example

The assistant is instructed not to invent Zepto policies or use information outside the retrieved context.

## API

Start the FastAPI backend locally:

```powershell
uvicorn main:app --reload
```

The API runs at:

```text
http://127.0.0.1:8000
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Retrieval Question

Request:

```json
{
  "query": "What are the delivery charges?"
}
```

Example response:

```json
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc_01.txt",
    "doc_05.txt",
    "doc_02.txt"
  ],
  "confidence": 1.0
}
```

### General Question

Request:

```json
{
  "query": "Tell me a joke"
}
```

Example response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

## Mock LLM Mode

The assistant runs in deterministic mock mode by default.

```powershell
$env:MOCK_LLM="1"
uvicorn main:app --reload
```

Mock mode:

- Does not require an external LLM API key.
- Produces deterministic answers.
- Uses retrieved context for policy questions.
- Returns a fixed response for general questions.

## Streamlit Frontend

Run the frontend from the project root:

```powershell
streamlit run support_assistant/app.py
```

The frontend is available at:

```text
http://localhost:8501
```

The Streamlit application sends questions to the FastAPI `/ask` endpoint and displays:

- The answer
- Retrieved source documents
- Confidence score

## Docker

Build the Docker image from the project root:

```powershell
docker build -t zepto-support-assistant ./support_assistant
```

Run the container:

```powershell
docker run --rm -p 7860:7860 zepto-support-assistant
```

Open the API documentation:

```text
http://127.0.0.1:7860/docs
```

The Docker image:

- Installs the Docker-compatible dependencies.
- Copies the assistant code and documents.
- Runs document ingestion during image creation.
- Starts FastAPI using Uvicorn on port `7860`.

## Response Schema

The API response follows a Pydantic model containing:

```json
{
  "answer": "string",
  "sources": ["string"],
  "confidence": 1.0
}
```

The confidence value is constrained between `0` and `1`.

## Technologies Used

- Python
- FastAPI
- Streamlit
- LangGraph
- ChromaDB
- Sentence Transformers
- Pydantic
- Docker