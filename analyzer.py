from rules import AMBIGUOUS_REPLACEMENTS, WEAK_MODALS

def analyze_requirement(text):
    issues = []
    text_lower = text.lower()

    for modal in WEAK_MODALS:
        if modal in text_lower:
            issues.append(f"Weak modal detected: '{modal}'")

    for word in AMBIGUOUS_REPLACEMENTS:
        if word in text_lower:
            issues.append(f"Ambiguous term detected: '{word}'")

    if " and " in text_lower:
        issues.append("Compound requirement detected (contains 'and')")

    if not any(char.isdigit() for char in text):
        issues.append("No measurable criteria detected")

    return issues