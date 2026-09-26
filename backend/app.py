"""
Phase 5: API Layer

Run this on your laptop with:
    uvicorn app:app --reload

Then open http://127.0.0.1:8000/docs in your browser -- FastAPI gives you
a free testing page automatically, no need to write a frontend yet.
"""

import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq
from rank_bm25 import BM25Okapi

CHROMA_DB_PATH = "data/chroma_store"
COLLECTION_NAME = "gov_schemes"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3
SIMILARITY_CUTOFF = 0.52   # raised from 0.45 -- three confirmed correct retrievals
                            # (typo'd/rephrased queries) landed at 0.473-0.503 and
                            # were being wrongly rejected; genuinely wrong matches
                            # observed at 0.62+, giving clear separation at 0.52
GROQ_MODEL = "openai/gpt-oss-20b"

load_dotenv()   # reads .env and loads its values into os.environ
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "PASTE_YOUR_KEY_HERE")

app = FastAPI(title="Government Scheme Assistant API")

# ---- CORS: without this, the browser blocks our React app from calling this API ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React's dev server address (Vite default)
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Loaded ONCE when the server starts, not on every question ----
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_collection(COLLECTION_NAME)
groq_client = Groq(api_key=GROQ_API_KEY)

# ---- BM25 keyword search setup (built once, at startup, same as everything above) ----
# We reuse the same 40 confirmed chunks that were embedded into Chroma, so both
# search methods are searching over the exact same set of chunks.
def load_confirmed_chunks(path="data/chunks.jsonl"):
    chunks = []
    with open(path) as f:
        for line in f:
            chunk = json.loads(line)
            if chunk["metadata"]["source_confidence"] == "confirmed":
                chunks.append(chunk)
    return chunks

confirmed_chunks = load_confirmed_chunks()
chunk_lookup = {c["chunk_id"]: c for c in confirmed_chunks}       # chunk_id -> full chunk
bm25_corpus_ids = [c["chunk_id"] for c in confirmed_chunks]
tokenized_corpus = [c["text"].lower().split() for c in confirmed_chunks]
bm25_index = BM25Okapi(tokenized_corpus)

RRF_K = 60                  # standard smoothing constant for Reciprocal Rank Fusion
SEMANTIC_CANDIDATES = 10    # how many candidates to pull from embedding search before fusing
BM25_CANDIDATES = 10        # how many candidates to pull from keyword search before fusing

# Semantic search is trusted more than BM25 here: BM25 has zero typo/rephrasing
# tolerance, so on a typo'd or loosely-worded query it can only ever contribute
# noise, not signal. Weighting it lower means it can still WIN when it finds a
# genuinely rare, exact term (e.g. "female"), but can't drown out a clean
# semantic match just by matching common words across unrelated chunks.
SEMANTIC_WEIGHT = 1.5
BM25_WEIGHT = 1.0
# NOTE: this ratio is a deliberate, tuned trade-off, not a "correct" universal value.
# 2.0 was too semantic-dominant (a strong BM25-only match could never surface at
# all). 1.0 (equal) let BM25 noise drown out clean semantic wins on typos. This
# is a genuine open question that should really be settled with a proper eval
# set (Phase 7, Part 3) rather than by testing single questions by hand.


# ---- What a question sent to our API must look like ----
class Question(BaseModel):
    question: str
    scheme_id: str | None = None   # optional -- only set if user picked a scheme


# ---- What our API sends back ----
class Answer(BaseModel):
    answer: str
    sources: list[str]
    confident: bool


def retrieve_chunks(question, filter_by_scheme=None):
    # ---- 1) Semantic search (embeddings, via Chroma) -- same as Phase 4/5 ----
    question_vector = embedding_model.encode([question]).tolist()
    where_clause = {"scheme_id": filter_by_scheme} if filter_by_scheme else None
    semantic_results = collection.query(
        query_embeddings=question_vector,
        n_results=SEMANTIC_CANDIDATES,
        where=where_clause,
    )
    semantic_ids = semantic_results["ids"][0]
    semantic_distances = semantic_results["distances"][0]
    semantic_rank = {chunk_id: rank for rank, chunk_id in enumerate(semantic_ids)}
    distance_lookup = dict(zip(semantic_ids, semantic_distances))

    # ---- 2) Keyword search (BM25) ----
    tokenized_question = question.lower().split()
    bm25_scores = bm25_index.get_scores(tokenized_question)
    scored = list(zip(bm25_corpus_ids, bm25_scores))
    if filter_by_scheme:  # same filtering idea as Chroma's `where`, applied after scoring
        scored = [
            (cid, score) for cid, score in scored
            if chunk_lookup[cid]["metadata"]["scheme_id"] == filter_by_scheme
        ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    bm25_rank = {chunk_id: rank for rank, (chunk_id, _) in enumerate(scored[:BM25_CANDIDATES])}

    # ---- 3) Combine both rankings with Reciprocal Rank Fusion ----
    candidate_ids = set(semantic_rank) | set(bm25_rank)
    combined_scores = {}
    for chunk_id in candidate_ids:
        score = 0.0
        if chunk_id in semantic_rank:
            score += SEMANTIC_WEIGHT / (RRF_K + semantic_rank[chunk_id])
        if chunk_id in bm25_rank:
            score += BM25_WEIGHT / (RRF_K + bm25_rank[chunk_id])
        combined_scores[chunk_id] = score

    ranked_ids = sorted(combined_scores, key=combined_scores.get, reverse=True)[:TOP_K]

    # ---- 4) Return in the same (id, text, distance, metadata) shape as before,
    #          plus one extra flag: was this a real embedding distance, or a
    #          BM25-only match (no Chroma distance available)?
    results = []
    for chunk_id in ranked_ids:
        chunk = chunk_lookup[chunk_id]
        has_real_distance = chunk_id in distance_lookup
        distance = distance_lookup.get(chunk_id, 1.0)
        results.append((chunk_id, chunk["text"], distance, chunk["metadata"], has_real_distance))
    return results


def build_prompt(question, chunks):
    context_text = "\n\n".join(
        f"[{meta['scheme_name']} - {meta['section']}]\n{doc}"
        for _, doc, _, meta, _ in chunks
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


# ---- The actual API endpoint ----
@app.post("/ask", response_model=Answer)
def ask_question(payload: Question):
    # ---- Case 1: retrieval itself finds nothing at all ----
    # Happens if scheme_id is wrong/typo'd -- the filter matches zero chunks.
    try:
        chunks = retrieve_chunks(payload.question, payload.scheme_id)
    except Exception:
        return Answer(
            answer="Something went wrong while searching for an answer. Please try again.",
            sources=[],
            confident=False,
        )

    if not chunks:
        return Answer(
            answer="I couldn't find any information for that (check the scheme_id, if you set one).",
            sources=[],
            confident=False,
        )

    # ---- Case 2: nothing retrieved is close enough to trust ----
    # We don't just check the #1 ranked chunk anymore. Because BM25 can push a
    # noisy keyword match to the top spot (e.g. generic word overlap), the
    # genuinely correct chunk might still be sitting at rank #2 or #3. So: look
    # at every chunk that HAS a real embedding distance, and take the best one.
    real_distances = [distance for _, _, distance, _, has_real in chunks if has_real]

    if real_distances:
        best_real_distance = min(real_distances)
        if best_real_distance > SIMILARITY_CUTOFF:
            return Answer(
                answer="I don't have reliable information to answer that.",
                sources=[],
                confident=False,
            )
    # If NO chunk has a real distance at all (every result was BM25-only),
    # we trust them -- they all earned their spot via genuine keyword matches.

    # ---- Case 3: the Groq API call itself fails (network, bad key, rate limit, etc.) ----
    system_message, user_message = build_prompt(payload.question, chunks)
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )
    except Exception as e:
        print(f"GROQ CALL FAILED: {e}")   # shows the real reason in your terminal
        return Answer(
            answer="I found relevant information, but couldn't generate an answer right now. Please try again.",
            sources=[chunk_id for chunk_id, _, _, _, _ in chunks],
            confident=False,
        )

    return Answer(
        answer=response.choices[0].message.content,
        sources=[chunk_id for chunk_id, _, _, _, _ in chunks],
        confident=True,
    )


@app.get("/")
def health_check():
    return {"status": "Government Scheme Assistant API is running"}
