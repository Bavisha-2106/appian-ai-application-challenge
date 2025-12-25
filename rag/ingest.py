import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

POLICY_DIR = "data/policies"
VECTOR_STORE_DIR = "rag/vector_store"


def clean_text(text: str) -> str:
    """Basic text cleanup for PDFs"""
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def ingest_all_pdfs():
    documents = []

    if not os.path.exists(POLICY_DIR):
        raise FileNotFoundError(f"Policy directory not found: {POLICY_DIR}")

    for file in os.listdir(POLICY_DIR):
        if not file.lower().endswith(".pdf"):
            continue

        path = os.path.join(POLICY_DIR, file)
        print(f"📄 Reading {file}")

        try:
            reader = PdfReader(path)
        except Exception as e:
            print(f"❌ Failed to read {file}: {e}")
            continue

        for page_no, page in enumerate(reader.pages):
            raw_text = page.extract_text()

            if not raw_text:
                continue

            text = clean_text(raw_text)

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file,
                        "page": page_no + 1
                    }
                )
            )

    print(f"✅ Loaded {len(documents)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    # Add chunk IDs
    for idx, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = idx

    print(f"✂️ Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTOR_STORE_DIR)

    print(f"💾 Vector store saved to {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    ingest_all_pdfs()
