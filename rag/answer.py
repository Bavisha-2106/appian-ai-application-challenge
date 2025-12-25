def generate_answer(docs):
    sections = {
        "procedure": [],
        "eligibility": [],
        "conditions": [],
        "escalation": [],
        "general": []
    }

    KEYWORDS = {
        "procedure": [
            "register", "apply", "application", "intake", "submit", "process"
        ],
        "eligibility": [
            "eligible", "eligibility", "rs.", "amount", "per hectare", "compensation"
        ],
        "conditions": [
            "not eligible", "subject to", "provided that", "only if", "excluding"
        ],
        "escalation": [
            "escalate", "appeal", "grievance", "senior", "district collector"
        ]
    }

    for doc in docs:
        text = doc.page_content
        text_lower = text.lower()

        item = {
            "text": text[:400],
            "source": doc.metadata.get("source"),
            "page": doc.metadata.get("page")
        }

        matched = False

        for section, keywords in KEYWORDS.items():
            if any(keyword in text_lower for keyword in keywords):
                sections[section].append(item)
                matched = True
                break

        if not matched:
            sections["general"].append(item)

    # Safety: if nothing useful found
    if all(len(v) == 0 for v in sections.values()):
        return {
            "message": "No relevant policy information found for this case."
        }

    return sections
