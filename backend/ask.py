"""
Phase 4: Retrieval + Generation

Run this on your laptop (needs your Groq API key + internet).

What this script does, step by step:
1. Turns your question into numbers (same as before)
2. Searches the database for the top 3 closest chunks
3. Checks if the best match is actually good enough (safety check)
4. If good enough -> builds a message with those chunks + your question,
   sends it to the LLM, prints the real answer
5. If not good enough -> tells you honestly instead of guessing
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

# ---- Simple settings you can tweak ----
CHROMA_DB_PATH = "data/chroma_store"
COLLECTION_NAME = "gov_schemes"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3                      # how many chunks to retrieve
SIMILARITY_CUTOFF = 0.45       # if best match's distance is above this, treat as "no good answer"
GROQ_MODEL = "openai/gpt-oss-20b"   

# Paste your key here, OR set it as an environment variable named GROQ_API_KEY
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


def retrieve_chunks(collection, model, question, filter_by_scheme=None):
    question_vector = model.encode([question]).tolist()
    where_clause = {"scheme_id": filter_by_scheme} if filter_by_scheme else None

    results = collection.query(
        query_embeddings=question_vector,
        n_results=TOP_K,
        where=where_clause,
    )

    chunks = list(zip(
        results["ids"][0],
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0],
    ))
    return chunks


def build_prompt(question, chunks):
    context_text = "\n\n".join(
        f"[{meta['scheme_name']} - {meta['section']}]\n{doc}"
        for _, doc, _, meta in chunks
    )

    system_message = (
        "You are a helpful assistant that answers questions about Indian "
        "government scholarship schemes. Only use the information given in "
        "the CONTEXT below to answer. If the answer is not in the context, "
        "say you don't have that information -- do not guess or make "
        "anything up."
    )

    user_message = f"CONTEXT:\n{context_text}\n\nQUESTION: {question}"

    return system_message, user_message


def ask(question, filter_by_scheme=None):
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    client_chroma = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client_chroma.get_collection(COLLECTION_NAME)

    chunks = retrieve_chunks(collection, model, question, filter_by_scheme)

    best_distance = chunks[0][2]  # lower distance = more similar (Chroma uses distance, not raw similarity)
    print(f"\nBest match distance: {best_distance:.4f} (lower is better; cutoff = {SIMILARITY_CUTOFF})")

    if best_distance > SIMILARITY_CUTOFF:
        print("\n>> No confident match found. Not calling the LLM.")
        print(">> Answer: I don't have reliable information to answer that.")
        return

    system_message, user_message = build_prompt(question, chunks)

    print("\nRetrieved chunks used as context:")
    for chunk_id, _, dist, meta in chunks:
        print(f"  - {chunk_id} (distance={dist:.4f})")

    groq_client = Groq(api_key=GROQ_API_KEY)
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    print("\n>> Answer:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    # Try a normal question
    ask("What is the income limit for Pragati?")

    # Try the tricky scheme-agnostic one from before
    ask("Am I eligible for a scholarship if I have a disability?")
