# Context-Aware Policy Retrieval with Verifiable Citations

### Team: Finding Nemo
**Appian AI Application Challenge 2026**

## Overview
This repository contains a **context-aware policy retrieval system** designed for complex, regulated case-management scenarios.  
The system assists agents by surfacing **case-specific policy guidance** with **direct, verifiable citations**, reducing manual policy lookup while maintaining auditability and trust.

The solution follows a **Retrieval-Augmented Generation (RAG)** approach and operates strictly within a **closed, policy-only knowledge domain**.

---

## Key Features
- Context-aware retrieval based on active case attributes (e.g., case type, sector, region)
- Source-grounded responses with direct references to policy documents and locations
- Closed knowledge domain to prevent reliance on unverified external information
- Simple UI for demonstrating agent interaction
- Designed for integration with regulated case-management workflows

---

## High-Level Workflow
1. Policy documents are processed and indexed into a vector-based knowledge store.
2. Case context is provided as input.
3. Relevant policy sections are retrieved based on contextual relevance.
4. Structured guidance is returned with verifiable citations.

---

## Project Structure
```text
appian-ai-application-challenge/
├── data/
│   └── policies/               # Sample policy PDFs (for demonstration only)
├── rag/
│   ├── ingest.py               # Policy ingestion and indexing logic
│   ├── retrieve.py             # Context-aware retrieval logic
│   └── answer.py               # Response generation with citations
├── app.py                      # Main application (UI / entry point)
├── requirements.txt
├── README.md
```
---
## How to Run (Local)

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Ingest Data (Build Vector Store)**
```bash
python rag/ingest.py
```

**Run the Application**
```bash
streamlit run app.py
```
---

## Team Members
#### Bavisha T J
#### S S Pavithra Thampi
