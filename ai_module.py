import numpy as np
import hashlib

class TransformerEmbeddingEngine:
    def generate_embedding(self, text):
        hash_val = int(hashlib.sha256(text.encode()).hexdigest(), 16)
        return np.array([(hash_val >> i) & 0xFF for i in range(0, 64, 8)])