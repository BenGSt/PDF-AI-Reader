"""Simple embeddings wrapper that tries to use sentence-transformers and falls back to a deterministic hashing-based vector.
This keeps the scaffold lightweight and testable without large model downloads.
"""
from typing import List


class Embeddings:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = None
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(model_name)
        except Exception:
            # model not available in scaffold environment
            self.model = None

    def embed(self, texts: List[str]):
        """Return list of vectors (lists of floats)."""
        if self.model is not None:
            return self.model.encode(texts, show_progress_bar=False)

        # Fallback: simple deterministic numeric vector (not suitable for production)
        vectors = []
        for t in texts:
            # convert chars to small numeric vector (sum of codepoints mod buckets)
            buckets = 64
            vec = [0.0] * buckets
            for i, ch in enumerate(t[:2048]):
                idx = (ord(ch) + i) % buckets
                vec[idx] += (i % 5 + 1) * 0.1
            # normalize
            norm = sum(x * x for x in vec) ** 0.5 or 1.0
            vec = [x / norm for x in vec]
            vectors.append(vec)
        return vectors
