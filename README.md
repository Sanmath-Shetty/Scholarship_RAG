# Government Scheme Assistant

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about 8
Indian government scholarship schemes, built end-to-end from scratch — no
framework abstractions for chunking, embedding, or retrieval.

Built as a placement portfolio project to demonstrate understanding of the
full RAG pipeline: data preparation, chunking strategy, embeddings, vector
search, hybrid search, generation, API design, and frontend integration.

---

## Schemes covered

- Central Sector Scheme of Scholarships (CSSS)
- AICTE Pragati (female students, technical education)
- AICTE Saksham (differently-abled students, technical education)
- Merit-cum-Means Scholarship (MCM)
- Post-Matric Scholarship — SC, ST, OBC, and Minority variants (modeled as
  4 separate schemes, since each has a different ministry and income ceiling)

---

## Architecture

```
Data (schemes_raw.py)
    -> Chunking (chunk_builder.py)              -> chunks.jsonl (48 chunks)
    -> Embeddings + Vector Store (build_vector_store.py)
         all-MiniLM-L6-v2 (384-dim) -> ChromaDB (cosine similarity)
    -> Hybrid Retrieval + Generation (inside app.py)
         semantic search (Chroma) + keyword search (BM25)
         -> combined via weighted Reciprocal Rank Fusion
         -> confidence cutoff check
         -> Groq-hosted LLM (openai/gpt-oss-20b) generates the answer
    -> API layer (FastAPI, app.py)
    -> Frontend (React, frontend/App.jsx)
```

---

## Development journey

This project was built in 7 phases, each building directly on the last.

**Phase 0 — Core RAG concepts.** Established the fundamental shift RAG makes:
an LLM as a reader answering from provided context, not a memorizer
recalling facts. Covered the two-pipeline architecture (offline indexing vs.
live query), semantic vs. keyword search, and cosine similarity.

**Phase 1 — Data collection.** Built structured source data for all 8
schemes, tagging every fact as CONFIRMED, NEEDS VERIFICATION, or GAP. Caught
and fixed two real data errors by cross-checking against official
scholarships.gov.in sources: the CSSS UG amount (corrected to Rs. 12,000/year)
and the MCM income ceiling (corrected to Rs. 2.5 lakh/year, which had been
contaminated by CSSS's own ceiling figure — an early, real-world preview of
the exact chunking-contamination problem chunking strategy exists to prevent).

**Phase 2 — Chunking strategy.** Chose structure-aware chunking (one chunk
per scheme-section pair) over fixed-size splitting. Modeled Post-Matric as 4
separate scheme-documents rather than one blended scheme, since SC/ST/OBC/
Minority variants have different ministries and income ceilings. Established
that metadata enables filtering but does not touch the embedding vector
itself — chunk text must explicitly restate the scheme name for the
embedding to carry scheme-specific signal. Produced 48 chunks (40 confirmed +
8 GAP).

**Phase 3 — Embeddings + vector store.** Chose `all-MiniLM-L6-v2` (fast,
CPU-friendly) and ChromaDB (embedded, metadata-filterable, cosine
similarity). Deliberately excluded GAP chunks from indexing. Verified real
embeddings fixed a genuine retrieval failure a TF-IDF prototype had shown
(literal "disabled" vs. "differently-abled" mismatch) — confirming why
semantic embeddings matter over pure keyword counting.

**Phase 4 — Retrieval + generation.** Wired up the full RAG loop: retrieve
top-3 chunks, check a similarity cutoff, and generate an answer via Groq only
if confident. The system prompt explicitly instructs the LLM to say "I don't
know" rather than guess. Discovered and documented that vector search always
returns its top-k results regardless of match quality — the distance cutoff
is what actually prevents confidently-wrong answers from bad retrievals.

**Phase 5 — API layer.** Wrapped the pipeline in FastAPI, loading the model,
vector store, and Groq client once at startup instead of per-request. Added
proper error handling for empty retrieval results and Groq API failures.
Debugged two real issues during testing: a stale/deprecated Groq model name,
and a missing API key — both traced by reading terminal error output rather
than guessing.

**Phase 6 — Frontend.** Built a React interface calling the FastAPI backend,
including CORS configuration (a real, common first speed bump when frontend
and backend run on separate addresses) and a scheme-filter dropdown to
trigger metadata filtering on demand. Confirmed semantic search's typo
tolerance live, in the actual UI.

**Phase 7 — Hardening and polish, in three parts:**
- *API key security*: moved the Groq key out of source code into a
  git-ignored `.env` file, so the codebase is safe to make public.
- *Hybrid search*: added BM25 keyword search alongside the existing semantic
  search, combined via weighted Reciprocal Rank Fusion. Found and fixed two
  real integration bugs in the process (BM25-only matches being unfairly
  rejected by a distance check designed for embeddings; BM25 noise
  displacing a correct chunk from rank #1 without the confidence check
  looking further down the list). Tuned the semantic/BM25 weight ratio and
  the similarity cutoff based on real evidence gathered from failing test
  cases, not guesswork.
- *Evals*: built a fixed 13-question test set and a script to measure
  retrieval hit rate and confidence pass rate in one run, replacing manual
  one-question-at-a-time testing with a repeatable, numeric process.

---

## Key design decisions

- **Structure-aware chunking** — one chunk per (scheme, section) pair, not
  fixed-size text splitting. Each Post-Matric variant (SC/ST/OBC/Minority) is
  modeled as its own scheme-document rather than one blended scheme, since
  each has a different ministry and income ceiling.
- **Metadata vs. embedding content** — metadata (`scheme_id`, `section`, etc.)
  enables filtering but does NOT affect the embedding vector. Chunk text
  explicitly restates the scheme name so the embedding itself carries
  scheme-specific signal.
- **GAP chunks excluded from retrieval** — 8 of 48 chunks are marked GAP
  (unverified facts) and are deliberately excluded from the vector store and
  BM25 index, so the system never retrieves unconfirmed information.
- **Hybrid search** — pure semantic search struggles with exact,
  meaning-flipping keywords (e.g. "female-only"); pure keyword search (BM25)
  has zero typo/rephrasing tolerance. Both are run and combined via weighted
  Reciprocal Rank Fusion (semantic weighted 1.5x over BM25's 1.0x — semantic
  is trusted more by default, BM25 acts as a booster for cases with a
  genuinely rare, distinctive term).
- **Two-part confidence check** — (1) a distance cutoff before the LLM even
  runs, catching queries where nothing retrieved is close enough; (2) a
  system prompt instruction telling the LLM to say "I don't know" rather than
  guess, catching cases where a chunk is topically similar but doesn't
  actually answer the question. The cutoff also correctly handles chunks that
  won via BM25 alone (no real embedding distance) — those are trusted rather
  than penalized for lacking a distance to check.
- **Environment-based secrets** — the Groq API key is loaded from a
  git-ignored `.env` file via `python-dotenv`, never hardcoded, so the
  codebase itself is safe to make public.

---

## Tech stack

| Layer | Choice |
|---|---|
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`, 384-dim) |
| Vector store | ChromaDB (persistent, cosine similarity) |
| Keyword search | BM25 (`rank_bm25`) |
| LLM | Groq API (`openai/gpt-oss-20b`) |
| Backend | FastAPI |
| Frontend | React (Vite) |

---

## Project structure

```
govscheme_rag/
├── data/
│   ├── schemes_raw.py       # source data, CONFIRMED/GAP tagged
│   └── chunks.jsonl         # 48 chunks (40 confirmed + 8 GAP)
├── frontend/
│   └── App.jsx              # React chat UI
├── chunk_builder.py         # builds chunks.jsonl from schemes_raw.py
├── build_vector_store.py    # embeds confirmed chunks into ChromaDB
├── ask.py                   # CLI script for quick testing
├── app.py                   # FastAPI backend (hybrid search + generation)
├── eval_questions.jsonl     # fixed test set for retrieval evals
├── eval_retrieval.py        # runs eval_questions.jsonl against real app.py logic
├── requirements.txt
├── .env                     # GROQ_API_KEY (git-ignored, not in repo)
└── .gitignore
```

---

## Setup

```bash
pip install -r requirements.txt

# Build the data + vector store (run once)
python chunk_builder.py
python build_vector_store.py

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the backend
uvicorn app:app --reload
```

In a separate terminal, for the frontend:
```bash
cd frontend
npm install
npm run dev
```
Open the address printed by `npm run dev` (typically `http://localhost:5173`).

---

## Evaluation results

Run with `python eval_retrieval.py`, against a 13-question test set covering
all 8 schemes plus specific edge cases (typos, exact keywords, rephrasing,
hard negatives):

- **Retrieval hit rate: 12/13 (92%)** — correct scheme's chunk retrieved
- **Confidence pass rate: 11/13 (85%)** — passed the similarity cutoff, so an
  answer was actually attempted

### Known limitations (found via eval, not hidden)

1. **"Which scheme allows lateral entry in the 2nd year?"** — retrieval miss.
   BM25 correctly ranked the right chunk highly, but semantic search missed
   it entirely from its own candidate list. Reciprocal Rank Fusion only
   considers rank position, not score magnitude, so it couldn't compensate.
   A learned reranker (instead of RRF) would likely fix this.

2. **"Is there support for differently-abled engineering students?"** —
   retrieved correctly, but failed the confidence cutoff (distance 0.673,
   solidly in "wrong match" territory based on other data points). Shorter
   phrasings of the same question score much better (~0.47). This reflects a
   real limitation of `all-MiniLM-L6-v2` — a small, fast embedding model that
   is more sensitive to sentence length/structure than a larger model would
   be. A stronger embedding model would likely close this gap.

These are documented rather than over-tuned against, since fixing them
"for real" would mean changing the embedding model or fusion algorithm, not
adjusting a threshold number.

---

## Possible future improvements

- Swap `all-MiniLM-L6-v2` for a larger, more accurate embedding model
- Replace RRF with a learned reranker (e.g. cross-encoder) for better fusion
- Expand the eval set for more statistically meaningful pass rates
- Add conversation history / multi-turn support to the frontend
