from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
DB_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "zepto_support"
MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=str(DB_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    documents = []
    ids = []
    metadatas = []

    for file_path in sorted(DOCS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            continue

        documents.append(text)
        ids.append(file_path.stem)
        metadatas.append(
            {
                "source": file_path.name,
                "path": str(file_path),
            }
        )

    if not documents:
        raise RuntimeError("No documents found in support_assistant/docs")

    print(f"Embedding {len(documents)} documents...")
    embeddings = model.encode(documents).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Successfully stored {len(documents)} documents.")
    print(f"ChromaDB location: {DB_DIR}")


if __name__ == "__main__":
    main()