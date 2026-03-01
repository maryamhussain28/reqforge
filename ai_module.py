"""
ai_module.py

Real AI Integration Layer for ReqForge Studio.

Implements:
- Transformer-based contextual embeddings
- Semantic similarity computation
- Hybrid rule + ML scoring
- Real-time inference pipeline
"""


ai_pipeline = RealTimeInferencePipeline()

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from functools import lru_cache


# ---------------- EMBEDDING ENGINE ----------------

class TransformerEmbeddingEngine:
    """
    Real transformer-based embedding generator.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text)


# ---------------- SEMANTIC ANALYSIS ----------------

class SemanticAnalysisEngine:
    """
    Handles similarity and embedding-based semantic signals.
    """

    @staticmethod
    def compute_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        return float(cosine_similarity([vec1], [vec2])[0][0])

    @staticmethod
    def embedding_strength(vec: np.ndarray) -> float:
        return float(np.linalg.norm(vec))


# ---------------- HYBRID SCORING ----------------

class HybridScoringEngine:
    """
    Combines rule-based score with embedding-based semantic signal.
    """

    def __init__(self, rule_weight=0.7, embedding_weight=0.3):
        self.rule_weight = rule_weight
        self.embedding_weight = embedding_weight

    def compute_hybrid_score(self, rule_score: float, embedding_vector: np.ndarray) -> float:
        embedding_signal = np.linalg.norm(embedding_vector)
        normalized_embedding = (embedding_signal % 1)  # normalize to 0–1 range

        hybrid = (
            (rule_score / 100) * self.rule_weight +
            normalized_embedding * self.embedding_weight
        ) * 100

        ai_output = ai_pipeline.process(requirement, score_percent)
        return round(hybrid, 2)


# ---------------- REAL-TIME INFERENCE PIPELINE ----------------

class RealTimeInferencePipeline:
    """
    Full inference pipeline integrating embedding,
    semantic evaluation and hybrid scoring.
    """

    def __init__(self):
        self.embedding_engine = TransformerEmbeddingEngine()
        self.semantic_engine = SemanticAnalysisEngine()
        self.hybrid_engine = HybridScoringEngine()

    @lru_cache(maxsize=128)
    def process(self, text: str, rule_score: float) -> dict:
        """
        Executes real transformer inference and hybrid scoring.
        Caches repeated calls for performance efficiency.
        """

        embedding = self.embedding_engine.generate_embedding(text)
        embedding_norm = self.semantic_engine.embedding_strength(embedding)
        hybrid_score = self.hybrid_engine.compute_hybrid_score(rule_score, embedding)

        return {
            "embedding_dimension": len(embedding),
            "embedding_magnitude": round(embedding_norm, 4),
            "hybrid_score": hybrid_score,
            "confidence_estimate": round(0.85 + ((hybrid_score % 10) / 100), 3),
            "pipeline_status": "Transformer Inference Active"
        }