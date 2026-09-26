"""
Phase 7, Part 3: Evals

Runs every question in eval_questions.jsonl through the REAL retrieve_chunks()
function from app.py (the exact same code your live API uses), and checks two
things per question:

  1. Retrieval hit  -- did a chunk from the expected scheme show up at all?
  2. Confidence pass -- did it pass SIMILARITY_CUTOFF (would the system
                        actually attempt an answer, or say "I don't know")?

Run this with:
    python eval_retrieval.py

NOTE: importing app.py runs its startup code too (loading the embedding
model, connecting to Chroma, building the BM25 index, etc.) -- same cost as
starting the real server, just without actually starting uvicorn.
"""

import json
from app import retrieve_chunks, SIMILARITY_CUTOFF


def load_eval_set(path="eval_questions.jsonl"):
    cases = []
    with open(path) as f:
        for line in f:
            cases.append(json.loads(line))
    return cases


def run_eval():
    cases = load_eval_set()
    retrieval_hits = 0
    confidence_passes = 0
    results = []

    for case in cases:
        question = case["question"]
        expected_scheme = case["expected_scheme"]
        category = case["category"]

        chunks = retrieve_chunks(question)

        retrieved_schemes = [meta["scheme_id"] for _, _, _, meta, _ in chunks]
        retrieval_hit = expected_scheme in retrieved_schemes

        real_distances = [distance for _, _, distance, _, has_real in chunks if has_real]
        if real_distances:
            best_distance = min(real_distances)
            confidence_pass = best_distance <= SIMILARITY_CUTOFF
        else:
            best_distance = None
            confidence_pass = True  # BM25-only results are trusted, per app.py logic

        if retrieval_hit:
            retrieval_hits += 1
        if confidence_pass:
            confidence_passes += 1

        results.append({
            "question": question,
            "category": category,
            "expected": expected_scheme,
            "retrieved": retrieved_schemes,
            "retrieval_hit": retrieval_hit,
            "best_distance": best_distance,
            "confidence_pass": confidence_pass,
        })

    # ---- Print a readable report ----
    print(f"\n{'='*70}")
    print(f"EVAL RESULTS -- {len(cases)} test cases")
    print(f"{'='*70}\n")

    for r in results:
        status = "PASS" if (r["retrieval_hit"] and r["confidence_pass"]) else "FAIL"
        dist_str = f"{r['best_distance']:.3f}" if r["best_distance"] is not None else "N/A"
        print(f"[{status}] ({r['category']}) {r['question']}")
        print(f"        expected={r['expected']}  retrieved={r['retrieved']}")
        print(f"        retrieval_hit={r['retrieval_hit']}  "
              f"confidence_pass={r['confidence_pass']}  best_distance={dist_str}\n")

    total = len(cases)
    print(f"{'='*70}")
    print(f"Retrieval hit rate:   {retrieval_hits}/{total} ({100*retrieval_hits/total:.0f}%)")
    print(f"Confidence pass rate: {confidence_passes}/{total} ({100*confidence_passes/total:.0f}%)")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    run_eval()
