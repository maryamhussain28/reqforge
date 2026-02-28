from rules import AMBIGUOUS_REPLACEMENTS, WEAK_MODALS
from ai_module import RealTimeInferencePipeline

# Initialize once (prevents reloading model repeatedly)
_ai_pipeline = RealTimeInferencePipeline()


def analyze_requirement(text):
    issues = []
    text_lower = text.lower()

    # ---------------- RULE-BASED CHECKS ----------------

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

    # ---------------- AI SEMANTIC SIGNAL (REAL) ----------------

    try:
        # Use current rule-based score proxy (10 - issue count)
        proxy_rule_score = max(100 - (len(issues) * 10), 0)

        ai_output = _ai_pipeline.process(text, proxy_rule_score)

        # Example semantic enrichment (does not change core logic)
        if ai_output["embedding_dimension"] < 100:
            issues.append("Low semantic richness detected")

        if ai_output["confidence_estimate"] < 0.9:
            issues.append("Contextual confidence below optimal threshold")

    except Exception:
        # Fail-safe: analysis should never crash
        issues.append("AI semantic evaluation skipped (fallback mode)")

    return issues