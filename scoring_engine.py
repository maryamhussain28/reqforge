# core/scoring_engine.py

import numpy as np

class HybridScoringEngine:
    """
    Multi-signal scoring:
    - Rule validation
    - Embedding similarity
    """

    def cosine_similarity(self, v1, v2):
        return np.dot(v1, v2) / (
            np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8
        )

    def rule_validation(self, text):
        required_keywords = ["shall", "must", "should"]
        score = sum(word in text for word in required_keywords)
        return score / len(required_keywords)

    def evaluate(self, original_text, structured_output, embedding_vector):
        rule_score = self.rule_validation(original_text)

        # Dummy semantic consistency score
        semantic_signal = np.mean(embedding_vector) % 1

        final_score = (0.5 * rule_score) + (0.5 * semantic_signal)

        return {
            "rule_score": rule_score,
            "semantic_signal": semantic_signal,
            "final_score": final_score
        }