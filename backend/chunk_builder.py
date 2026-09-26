"""
Phase 2: Chunking

Converts the raw structured scheme data (data/schemes_raw.py) into a flat
list of chunk records, ready to be embedded in Phase 3.
"""

import json
from pathlib import Path
from data.schemes_raw import SCHEMES

OUTPUT_PATH = Path(__file__).parent / "data" / "chunks.jsonl"


def build_chunks(schemes):
    chunks = []
    skipped_gaps = []

    for scheme in schemes:
        scheme_id = scheme["scheme_id"]
        scheme_name = scheme["scheme_name"]
        scheme_category = scheme["scheme_category"]

        for section_name, text in scheme["sections"].items():
            chunk_id = f"{scheme_id}__{section_name}"
            is_gap = text.strip().startswith("GAP:")

            chunk = {
                "chunk_id": chunk_id,
                "text": text.strip(),
                "metadata": {
                    "scheme_id": scheme_id,
                    "scheme_name": scheme_name,
                    "scheme_category": scheme_category,
                    "section": section_name,
                    "source_confidence": "gap" if is_gap else "confirmed",
                },
            }

            if is_gap:
                skipped_gaps.append(chunk_id)
            chunks.append(chunk)

    return chunks, skipped_gaps


def main():
    chunks, skipped_gaps = build_chunks(SCHEMES)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    total = len(chunks)
    gap_count = len(skipped_gaps)
    confirmed_count = total - gap_count

    print(f"Built {total} total chunks -> {OUTPUT_PATH}")
    print(f"  {confirmed_count} confirmed chunks (ready to embed)")
    print(f"  {gap_count} GAP chunks (flagged, not fact-verified)")


if __name__ == "__main__":
    main()
