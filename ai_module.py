import numpy as np
import hashlib
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingEngine:
    """
    Modular embedding engine supporting multiple embedding strategies.

    Current modes:
        - 'hash'         : Deterministic pseudo-embedding (default)
        - 'transformer'  : Placeholder for real transformer integration

    Designed for extensibility without modifying the evaluation pipeline.
    """

    def __init__(self, mode: str = "hash"):
        self.mode = mode

        # Placeholder for future transformer model
        # Example future integration:
        # from sentence_transformers import SentenceTransformer
        # self.model = SentenceTransformer('all-MiniLM-L6-v2')

    # -------------------------
    # Public Interface
    # -------------------------

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate fixed-dimensional embedding based on selected mode.
        """
        if self.mode == "hash":
            return self._hash_embedding(text)

        elif self.mode == "transformer":
            return self._transformer_embedding(text)

        else:
            raise ValueError(f"Unsupported embedding mode: {self.mode}")

    def compute_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.
        """
        vec1 = self._normalize(vec1)
        vec2 = self._normalize(vec2)

        return float(cosine_similarity([vec1], [vec2])[0][0])

    # -------------------------
    # Hash-Based Embedding
    # -------------------------

    def _hash_embedding(self, text: str) -> np.ndarray:
        """
        Deterministic pseudo-embedding using SHA-256 hashing.
        Provides reproducible fixed-dimensional vector.
        """
        hash_val = int(hashlib.sha256(text.encode()).hexdigest(), 16)

        # Extract 16 bytes → 16-dimensional embedding
        embedding = np.array(
            [(hash_val >> i) & 0xFF for i in range(0, 128, 8)],
            dtype=np.float32
        )

        return self._normalize(embedding)

    # -------------------------
    # Transformer Placeholder
    # -------------------------

    def _transformer_embedding(self, text: str) -> np.ndarray:
     
    

        raise NotImplementedError(
            "Transformer mode not yet integrated. "
            "Designed for future SentenceTransformer/HuggingFace integration."
        )

    # -------------------------
    # Utility Functions
    # -------------------------

    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        """
        Normalize embedding vector (L2 normalization).
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm