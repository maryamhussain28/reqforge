from rules import AMBIGUOUS_REPLACEMENTS, WEAK_MODALS
from rules import AMBIGUOUS_REPLACEMENTS, WEAK_MODALS

# Safe AI import
try:
    from ai_module import RealTimeInferencePipeline
    _ai_pipeline = RealTimeInferencePipeline()
except Exception:
    _ai_pipeline = None


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

    # ---------------- AI SEMANTIC SIGNAL (SAFE) ----------------

    if _ai_pipeline:
        try:
            proxy_rule_score = max(100 - (len(issues) * 10), 0)
            ai_output = _ai_pipeline.process(text, proxy_rule_score)

            # Enrichment only — does NOT change core scoring
            if ai_output.get("embedding_dimension", 0) < 8:
                issues.append("Low semantic richness detected")

            if ai_output.get("confidence_estimate", 1) < 0.85:
                issues.append("Contextual confidence below optimal threshold")

        except Exception:
            issues.append("AI semantic evaluation skipped (fallback mode)")

    return issues