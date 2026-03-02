# core/structuring_engine.py

class RequirementStructurer:
    """
    Transforms informal text into structured format.
    Layer 3: Transformation logic.
    """

    def structure(self, clauses):
        structured = []

        for clause in clauses:
            structured.append({
                "actor": "System",
                "action": clause.strip(),
                "condition": "When applicable",
                "measurable": True
            })

        return structured