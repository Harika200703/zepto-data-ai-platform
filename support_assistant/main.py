import os
from typing import List, TypedDict

import chromadb
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "zepto_support"

app = FastAPI(title="Zepto Support Assistant")

embedding_model = SentenceTransformer(MODEL_NAME)

chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_collection(COLLECTION_NAME)

MOCK_LLM = os.getenv("MOCK_LLM", "1") == "1"


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float


class AssistantState(TypedDict, total=False):
    question: str
    intent: str
    answer: str
    sources: List[str]
    confidence: float


def classify_intent(state: AssistantState):
    question = state["question"].lower()

    keywords = {
        "delivery": ["delivery", "deliver", "minutes", "pin code"],
        "return_refund": ["return", "refund", "damaged", "spoiled", "missing"],
        "membership": ["pass", "membership", "basic", "subscription"],
        "tracking": ["track", "rider", "tracking", "late", "delay"],
        "cancellation": ["cancel", "cancellation"],
        "gift_card": ["gift card", "giftcard"],
        "support": ["support", "chat", "email", "phone"],
    }

    for intent, words in keywords.items():
        if any(word in question for word in words):
            return {"intent": intent}

    return {"intent": "general"}


def retrieve_documents(question: str):
    query_embedding = embedding_model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    sources = [
        metadata.get("source", "unknown")
        for metadata in metadatas
    ]

    return documents, sources, distances


def build_prompt(question: str, documents: List[str]) -> str:
    context = "\n\n".join(documents)

    return f"""
Role:
You are a helpful Zepto customer-support assistant.

Context:
Use only the supplied knowledge-base context.

Task:
Answer the customer's question accurately and clearly.

Constraints:
- Do not invent policies or information.
- If the context does not contain the answer, say that the information is unavailable.
- Do not mention internal implementation details.

Question:
{question}

Knowledge-base context:
{context}

Format:
Give a direct, easy-to-understand answer.

Length:
Keep the answer concise, preferably 2 to 5 sentences.

Example:
Question: Can I cancel an order after it is packed?
Answer: Orders can be cancelled free of cost before they are packed. Once an order is packed, it cannot normally be cancelled through the app.
"""


def mock_answer(question: str, documents: List[str]) -> str:
    if not documents:
        return "Sorry, I could not find information related to your question."

    return (
        "Based on the Zepto support information: "
        + documents[0]
    )


def retrieve_and_answer(state: AssistantState):
    documents, sources, distances = retrieve_documents(
        state["question"]
    )

    prompt = build_prompt(state["question"], documents)

    if MOCK_LLM:
        answer = mock_answer(state["question"], documents)
    else:
        answer = (
            "Real LLM mode is not configured yet. "
            "Please use MOCK_LLM=1 or configure an LLM provider."
        )

    confidence = 0.85 if documents else 0.20

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }


def direct_answer(state: AssistantState):
    return {
        "answer": (
            "Please contact Zepto support through in-app chat "
            "for assistance with this question."
        ),
        "sources": [],
        "confidence": 0.40,
    }


def route_intent(state: AssistantState):
    if state.get("intent") == "general":
        return "direct_answer"

    return "retrieve_and_answer"


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
        {"question": request.question}
    )

    return AskResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 0.0),
    )