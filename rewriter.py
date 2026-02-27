from rules import AMBIGUOUS_REPLACEMENTS, WEAK_MODALS

def rewrite_requirement(text):
    explanation = []
    text_lower = text.lower()

    # Normalize modal verbs
    for modal, replacement in WEAK_MODALS.items():
        if modal in text_lower:
            text = text.replace(modal, replacement)
            explanation.append(f"Replaced '{modal}' with '{replacement}'")

    # Replace ambiguous terms
    for word, replacement in AMBIGUOUS_REPLACEMENTS.items():
        if word in text_lower:
            text = text.replace(word, replacement)
            explanation.append(f"Replaced vague term '{word}' with measurable criterion")

    # Split compound requirements
    if " and " in text:
        parts = text.split(" and ")
        text = ". ".join(part.strip().capitalize() for part in parts)
        explanation.append("Split compound requirement into atomic statements")

    return text, explanation