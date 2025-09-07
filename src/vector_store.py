"""A tiny in-memory vector store with simple cosine-similarity search for MVP scaffolding.
Replace with ChromaDB in the integration phase.
"""
from typing import List, Dict, Any, Tuple

try:
    import numpy as np
except Exception:
    np = None


class SimpleVectorStore:
    def __init__(self):
        self.items = []  # list of dicts: {id, text, vector, metadata}

    def add(self, doc_id: str, text: str, vector, metadata: Dict[str, Any] = None):
        self.items.append({"id": doc_id, "text": text, "vector": vector, "metadata": metadata or {}})

    def _cosine_sim(self, a, b):
        if np is not None:
            a = np.array(a, dtype=float)
            b = np.array(b, dtype=float)
            denom = (np.linalg.norm(a) * np.linalg.norm(b))
            if denom == 0:
                return 0.0
            return float(np.dot(a, b) / denom)
        # fallback simple dot / (len) approximation
        try:
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5 or 1.0
            norm_b = sum(x * x for x in b) ** 0.5 or 1.0
            return dot / (norm_a * norm_b)
        except Exception:
            return 0.0

    def search(self, query_vector, top_k: int = 5) -> List[Tuple[float, dict]]:
        scores = []
        for item in self.items:
            score = self._cosine_sim(query_vector, item["vector"]) if item.get("vector") is not None else 0.0
            scores.append((score, item))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]

    def list_documents(self) -> List[Dict[str, Any]]:
        """Return list of all documents with their metadata."""
        return [
            {
                "id": item["id"],
                "source": item["metadata"].get("source", "unknown"),
                "text_length": len(item["text"]),
                "metadata": item["metadata"]
            }
            for item in self.items
        ]

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document by ID. Returns True if found and removed."""
        for i, item in enumerate(self.items):
            if item["id"] == doc_id:
                self.items.pop(i)
                return True
        return False


# convenience singleton for quick CLI usage in scaffold
_default_store = SimpleVectorStore()


def get_default_store():
    return _default_store
