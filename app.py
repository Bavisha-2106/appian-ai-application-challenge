import streamlit as st
import os
from rag.retrieve import retrieve_relevant_docs
from rag.answer import generate_answer

st.set_page_config(
    page_title="Just-in-Time Knowledge Assistant",
    layout="centered"
)

st.title("Just-in-Time Knowledge Assistant")
st.caption("Context-aware SDRF policy guidance for Indian disaster claims")

# ---------------- SESSION STATE ----------------
if "results" not in st.session_state:
    st.session_state.results = None

# ---------------- INPUT ----------------
st.subheader("Active Case Context")

claim_type = st.selectbox(
    "Disaster Type",
    ["Flood", "Drought", "Cyclone", "Earthquake"]
)

sector = st.selectbox(
    "Sector",
    ["Agriculture", "Animal Husbandry"]
)

state = st.selectbox(
    "State",
    [
        "Tamil Nadu",
        "Kerala",
        "Andhra Pradesh",
        "Karnataka",
        "Odisha",
        "West Bengal"
    ]
)

if st.button("Get Relevant Policy Guidance"):
    case = {
        "claim_type": claim_type,
        "sector": sector,
        "state": state
    }

    with st.spinner("Retrieving relevant policy guidance..."):
        docs = retrieve_relevant_docs(case)
        st.session_state.results = generate_answer(docs)

# ---------------- OUTPUT ----------------
def show_section(title, items):
    if not items:
        return

    st.subheader(title)
    for i, item in enumerate(items):
        st.write(f"- {item['text']}...")
        st.caption(
            f"Source: {item['source']} | Page {item['page']}"
        )

        if st.button(
            f"📄 Open PDF (Page {item['page']})",
            key=f"{item['source']}_{item['page']}_{i}"
        ):
            pdf_path = os.path.abspath(
                f"data/policies/{item['source']}"
            )
            os.startfile(pdf_path)

if st.session_state.results:
    results = st.session_state.results

    if isinstance(results, dict) and "message" in results:
        st.warning(results["message"])
    else:
        show_section("📌 What the agent should do", results.get("procedure"))
        show_section("🌾 Compensation eligibility", results.get("eligibility"))
        show_section("⚠️ Important conditions", results.get("conditions"))
        show_section("🚨 Escalation rules", results.get("escalation"))
