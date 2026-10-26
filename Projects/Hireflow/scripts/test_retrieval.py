"""
Run: python scripts/test_retrieval.py

Tests the full retrieval pipeline:
    JD text → embed → Pinecone search → rerank → top candidates

You can edit the JD_TEXT below to test different roles.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retrieval.chain import retrieve

# ── Edit this JD to test different roles ────────────────────────────
JD_TEXT = """
We are looking for a Senior Accountant to join our finance team.

Requirements:
- 3+ years of accounting experience
- Strong knowledge of financial reporting and general ledger
- Experience with month-end closing and bank reconciliation
- Proficiency in accounting software (SAP, NetSuite, or similar)
- CPA certification preferred
- Experience with variance analysis and budget planning
- Strong attention to detail and analytical skills

Responsibilities:
- Prepare and review financial statements
- Manage accounts receivable and payable
- Perform month-end and year-end close procedures
- Ensure compliance with accounting standards
- Support internal and external audits
"""


def main():
    
    print("=" * 50)
    print("HIREFLOW — RETRIEVAL TEST")
    print("=" * 50)
    print(f"\nJD Preview: {JD_TEXT[:100].strip()}...")

    # Run retrieval
    candidates = retrieve(jd_text=JD_TEXT, top_k=5)

    if not candidates:
        print("\nNo candidates found. Make sure resumes are ingested first.")
        print("Run: python scripts/test_ingestion.py resume/")
        return

    # Display results
    print("\n" + "=" * 50)
    print("TOP CANDIDATES")
    print("=" * 50)

    for i, c in enumerate(candidates):
        print(f"\nRank #{i + 1}")
        print(f"  File          : {c['file_name']}")
        print(f"  Candidate ID  : {c['candidate_id']}")
        print(f"  Vector score  : {c['score']}")
        print(f"  Rerank score  : {c['rerank_score']}")
        print(f"  Text preview  : {c['text'][:200].strip()}...")

    print("\nRetrieval test complete!")


if __name__ == "__main__":
    main()