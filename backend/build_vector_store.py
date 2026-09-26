"""
Phase 3: Embeddings + Vector Store

Reads data/chunks.jsonl (built in Phase 2), computes an embedding for each
confirmed chunk using sentence-transformers, and stores everything in a
persistent ChromaDB collection.

Design decisions carried forward from Phase 2:
- GAP chunks (source_confidence == "gap") are excluded from the embedded
  collection by default -- we don't want an unverified fact retrievable
  and presented to a user as if it were confirmed.
- Every chunk keeps its full metadata (scheme_id, scheme_name,
  scheme_category, section, source_confidence) attached in Chroma, so
  Phase 4 can do metadata-filtered retrieval, not just raw vector search.
"""

import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path(__file__).parent / "data" / "chunks.jsonl"
CHROMA_DB_PATH = Path(__file__).parent / "data" / "chroma_store"
COLLECTION_NAME = "gov_schemes"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks(path):
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks


def main():
    print(f"Loading chunks from {CHUNKS_PATH} ...")
    all_chunks = load_chunks(CHUNKS_PATH)

    # Exclude GAP chunks from the embeddable set -- see module docstring.
    embeddable_chunks = [
        c for c in all_chunks if c["metadata"]["source_confidence"] != "gap"
    ]
    gap_chunks = [c for c in all_chunks if c["metadata"]["source_confidence"] == "gap"]

    print(f"  {len(all_chunks)} total chunks found")
    print(f"  {len(embeddable_chunks)} confirmed chunks will be embedded")
    print(f"  {len(gap_chunks)} GAP chunks excluded (unverified, not indexed)")

    print(f"\nLoading embedding model '{EMBEDDING_MODEL_NAME}' ...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    print(f"  Embedding dimension: {model.get_sentence_embedding_dimension()}")

    texts = [c["text"] for c in embeddable_chunks]
    ids = [c["chunk_id"] for c in embeddable_chunks]
    metadatas = [c["metadata"] for c in embeddable_chunks]

    print(f"\nComputing embeddings for {len(texts)} chunks ...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    print(f"  Produced embeddings of shape: {embeddings.shape}")

    print(f"\nInitializing persistent ChromaDB at {CHROMA_DB_PATH} ...")
    client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

    # Fresh start each time this script runs, so re-running it after editing
    # schemes_raw.py always reflects the latest data rather than silently
    # accumulating duplicates.
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"  Deleted existing collection '{COLLECTION_NAME}' (fresh rebuild)")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # explicit: use cosine similarity
    )

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas,
    )

    print(f"\nDone. Collection '{COLLECTION_NAME}' now contains {collection.count()} chunks.")


if __name__ == "__main__":
    main()
