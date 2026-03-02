# core/embedding_engine.py

import hashlib
import numpy as np

class HashEmbeddingEngine:
    """
    Lightweight pseudo-embedding generator.
    Used to simulate contextual semantic representation.
    """

    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def _hash_to_vector(self, text: str):
        hash_digest = hashlib.sha256(text.encode()).hexdigest()

        # Convert hash into deterministic numeric vector
        vector = [
            int(hash_digest[i:i+4], 16) % 1000
            for i in range(0, len(hash_digest), 4)
        ]

        vector = vector[:self.dimension]
        return np.array(vector, dtype=float)

    def generate(self, text: str):
        return self._hash_to_vector(text)