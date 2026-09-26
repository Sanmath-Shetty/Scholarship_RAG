"""
Phase 3 test script -- query your REAL embeddings (run this on your laptop,
after build_vector_store.py has already run successfully).

Shows two ways to search:
1. No filter -- searches across ALL schemes
2. With filter -- searches ONLY within one scheme
"""

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DB_PATH = "data/chroma_store"
COLLECTION_NAME = "gov_schemes"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


def search(collection, model, question, filter_by_scheme=None, n_results=3):
    # Step 1: turn the question into the same kind of 384 numbers
    question_vector = model.encode([question]).tolist()

    # Step 2: build the filter, if one was asked for
    # This is the ONLY line that changes between filtered and unfiltered search
    where_clause = {"scheme_id": filter_by_scheme} if filter_by_scheme else None

    # Step 3: ask ChromaDB for the closest matches
    results = collection.query(
        query_embeddings=question_vector,
        n_results=n_results,
        where=where_clause,   # <-- this is metadata filtering. None = no filter.
    )

    print(f"\nQuestion: \"{question}\"")
    print(f"Filter used: {filter_by_scheme or 'none (searched everything)'}")
    for chunk_id, meta in zip(results["ids"][0], results["metadatas"][0]):
        print(f"  -> {chunk_id}   (scheme: {meta['scheme_name']})")


def main():
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    # TEST 1: no scheme mentioned -- let's see if the real model picks Saksham correctly
    search(collection, model,
           "eligibility for disabled students in technical education")

    # TEST 2: same question, but now FORCED to only look inside Pragati
    # (useful when your app already knows which scheme the user picked,
    # e.g. from a dropdown, or the user said the scheme name directly)
    search(collection, model,
           "eligibility for disabled students in technical education",
           filter_by_scheme="aicte_pragati")


if __name__ == "__main__":
    main()
