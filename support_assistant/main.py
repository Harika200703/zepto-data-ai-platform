import os
from typing import List, TypedDict

import chromadb
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "zepto_support"

MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"

app = FastAPI(title="Zepto Support Assistant")

embedding_model = SentenceTransformer(MODEL_NAME)

chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_collection(COLLECTION_NAME)


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1)


class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float = Field(..., ge=0.0, le=1.0)


class AssistantState(TypedDict, total=False):
    query: str
    intent: str
    answer: str
    sources: List[str]
    confidence: float


def classify_intent(state: AssistantState):
    query = state["query"].lower()

    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours",
    ]

    if any(keyword in query for keyword in policy_keywords):
        intent = "policy_question"
    else:
        intent = "general_question"

    return {"intent": intent}


def retrieve_documents(query: str):
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    sources = [
        metadata.get("source", "unknown")
        for metadata in metadatas
    ]

    return documents, sources


def build_prompt(query: str, documents: List[str]) -> str:
    context = "\n\n".join(documents)

    return f"""
Role:
You are a helpful Zepto customer-support assistant.

Context:
Use only the supplied Zepto policy context.

Task:
Answer the customer's query accurately using the retrieved context.

Negative constraints:
- Do not answer using information not present in the provided context.
- Do not invent policies, prices, timings, or services.
- If the context does not contain the answer, clearly say that the information is unavailable.

Format:
Give a direct and easy-to-understand answer.

Length:
Keep the answer concise, preferably 2 to 5 sentences.

Few-shot example:
Query: Can I cancel my order after it is packed?
Answer: Orders can be cancelled before they are packed. Once an order is packed, it cannot normally be cancelled through the app.

Customer query:
{query}

Retrieved context:
{context}
"""


def mock_policy_answer(documents: List[str]) -> str:
    if not documents:
        return "Sorry, I could not find information related to your question."

    top_chunk_snippet = documents[0][:200]

    return f"Based on the retrieved context: {top_chunk_snippet}"


def retrieve_and_answer(state: AssistantState):
    documents, sources = retrieve_documents(state["query"])

    prompt = build_prompt(state["query"], documents)

    if MOCK_LLM:
        answer = mock_policy_answer(documents)
    else:
        answer = (
            "Real LLM mode is not configured yet. "
            "The structured prompt is ready for LLM integration."
        )

    return {
        "answer": answer,
        "sources": sources,
        "confidence": 1.0,
    }


def direct_answer(state: AssistantState):
    if MOCK_LLM:
        answer = (
            "I can only answer questions about Zepto policies right now."
        )
    else:
        answer = (
            "Real LLM mode is not configured yet for general questions."
        )

    return {
        "answer": answer,
        "sources": [],
        "confidence": 1.0,
    }


def route_intent(state: AssistantState):
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


graph_builder = StateGraph(AssistantState)

graph_builder.add_node("classify_intent", classify_intent)
graph_builder.add_node("retrieve_and_answer", retrieve_and_answer)
graph_builder.add_node("direct_answer", direct_answer)

graph_builder.set_entry_point("classify_intent")

graph_builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    },
)

graph_builder.add_edge("retrieve_and_answer", END)
graph_builder.add_edge("direct_answer", END)

assistant_graph = graph_builder.compile()


@app.get("/")
def root():
    return {
        "message": "Zepto Support Assistant is running"
    }


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    result = assistant_graph.invoke(
        {"query": request.query}
    )

    return AskResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 1.0),
    )