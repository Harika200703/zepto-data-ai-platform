# Zepto Support Assistant

A Retrieval-Augmented Generation (RAG) customer-support assistant for Zepto.

## Features

- Uses 8 Zepto support documents as a knowledge base
- Generates embeddings using `all-MiniLM-L6-v2`
- Stores and retrieves documents using ChromaDB
- Uses LangGraph for intent classification and routing
- Provides a FastAPI `/ask` endpoint
- Returns answers, source documents, and confidence scores
- Supports mock LLM mode by default

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
      +----------------------+
      |                      |
      v                      v
Retrieve Documents      Direct Answer
      |
      v
ChromaDB Similarity Search
      |
      v
Answer + Sources + Confidence