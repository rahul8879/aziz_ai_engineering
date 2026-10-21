"""
Run: python scripts/test_ingestion.py <path_to_resume.pdf>

Example:
    python scripts/test_ingestion.py resumes/john_doe.pdf

Tests the full ingestion pipeline for a single resume:
  Load → Chunk → Email extract → Dedup → Embed → Upsert to Pinecone
"""
"""
Run with single file:
    python scripts/test_ingestion.py resume/john_doe.pdf

Run with folder (all PDFs):
    python scripts/test_ingestion.py resume/
"""
import sys
import os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.pipeline import ingest_resume
from pinecone import Pinecone
from config import settings


def verify_pinecone(candidate_id: str):
    pc = Pinecone(api_key=settings.pinecone_api_key)
    index = pc.Index(settings.pinecone_index_name)

    stats = index.describe_index_stats()
    print(f"\n  Total vectors in index: {stats.total_vector_count}")

    fetch_result = index.fetch(ids=[f"{candidate_id}_0"])
    if fetch_result.vectors:
        vec = fetch_result.vectors[f"{candidate_id}_0"]
        print(f"  Sample vector ID      : {vec.id}")
        print(f"  Dimensions            : {len(vec.values)}")
        print(f"  Metadata              : {vec.metadata}")
    else:
        print("  Warning: Vector not found — may still be indexing")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python scripts/test_ingestion.py resume/john.pdf   # single file")
        print("  python scripts/test_ingestion.py resume/            # full folder")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    # Collect PDF files
    if input_path.is_dir():
        pdf_files = sorted(input_path.glob("*.pdf"))
        if not pdf_files:
            print(f"No PDF files found in: {input_path}")
            sys.exit(1)
        print(f"Found {len(pdf_files)} PDF(s) in folder: {input_path}\n")
    elif input_path.is_file() and input_path.suffix.lower() == ".pdf":
        pdf_files = [input_path]
    else:
        print(f"Invalid path: {input_path}")
        print("Must be a .pdf file or a folder containing PDFs")
        sys.exit(1)

    # Process each PDF
    results = []
    for pdf in pdf_files:
        try:
            result = ingest_resume(str(pdf))
            results.append(result)
        except Exception as e:
            print(f"  ERROR processing {pdf.name}: {e}")
            results.append({
                "file_name": pdf.name,
                "status": "failed",
                "error": str(e)
            })

    # Summary
    print("\n" + "=" * 50)
    print("INGESTION SUMMARY")
    print("=" * 50)
    success = [r for r in results if r.get("status") == "success"]
    failed  = [r for r in results if r.get("status") == "failed"]

    print(f"  Total   : {len(results)}")
    print(f"  Success : {len(success)}")
    print(f"  Failed  : {len(failed)}")

    print("\nResults:")
    for r in results:
        if r.get("status") == "success":
            print(f"  ✓ {r['file_name']:<30} id: {r['candidate_id']}  chunks: {r['chunks']}")
        else:
            print(f"  ✗ {r['file_name']:<30} ERROR: {r.get('error')}")

    # Verify last successful one in Pinecone
    if success:
        last = success[-1]
        print(f"\nVerifying last ingested candidate in Pinecone...")
        verify_pinecone(last["candidate_id"])

    print("\nDone!")


if __name__ == "__main__":
    main()