from rag.retrieve import retrieve_relevant_docs
from rag.answer import generate_answer

case = {
    "claim_type": "Flood",
    "sector": "Agriculture",
    "state": "Tamil Nadu"
}

docs = retrieve_relevant_docs(case)
sections = generate_answer(docs)

for key, items in sections.items():
    print(f"\n--- {key.upper()} ---")
    for item in items:
        print(item["text"][:200])
        print(f"Source: {item['source']} | Page {item['page']}")
