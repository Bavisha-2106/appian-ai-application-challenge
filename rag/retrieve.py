from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_STORE_DIR = "rag/vector_store"


def build_query(case_context: dict) -> str:
    parts = []

    if case_context.get("claim_type"):
        parts.append(f"Disaster type: {case_context['claim_type']}")

    if case_context.get("sector"):
        parts.append(f"Sector: {case_context['sector']}")

    if case_context.get("state"):
        parts.append(f"State: {case_context['state']}")

    # IMPORTANT: force policy-specific retrieval
    parts.append(
        "specific SDRF compensation amounts, eligibility criteria, sector-wise norms, exclusions"
    )

    return ". ".join(parts)


def retrieve_relevant_docs(case_context: dict, k: int = 6):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        VECTOR_STORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )

    query = build_query(case_context)

    docs_with_scores = db.similarity_search_with_score(query, k=k)

    filtered_docs = []
    for doc, score in docs_with_scores:
        # Skip weak matches
        if score >= 0.8:
            continue

        # Skip generic SOP intro page
        if (
            doc.metadata.get("source") == "Claims_Processing_SOP_Internal.pdf"
            and doc.metadata.get("page") == 1
        ):
            continue

        filtered_docs.append(doc)

    print("🔍 Retrieval query:", query)
    for d in filtered_docs:
        print(f"📄 {d.metadata}")

    return filtered_docs
