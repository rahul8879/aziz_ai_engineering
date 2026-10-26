from pinecone import Pinecone, ServerlessSpec
from config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

pc.create_index(
    name = "hireflow-resumes",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
    )

