# core/preprocessing.py

import re

class RequirementPreprocessor:
    """
    Handles normalization and linguistic preparation.
    Layer 1: Pure preprocessing logic.
    """

    def normalize(self, text: str) -> str:
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text.lower()

    def extract_candidate_clauses(self, text: str):
        """
        Dummy clause splitting.
        """
        return text.split(" and ")

    def preprocess(self, text: str):
        normalized = self.normalize(text)
        clauses = self.extract_candidate_clauses(normalized)

        return {
            "normalized_text": normalized,
            "clauses": clauses
        }