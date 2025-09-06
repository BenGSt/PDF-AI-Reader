from src.embeddings import Embeddings
from src.vector_store import SimpleVectorStore


def test_query_returns_result():
    store = SimpleVectorStore()
    emb = Embeddings()

    texts = [
        "Cats are small domesticated carnivores.",
        "Dogs are loyal and friendly animals.",
        "Python is a programming language commonly used for ML and data science.",
    ]
    vecs = emb.embed(texts)
    for i, t in enumerate(texts):
        store.add(f"doc{i}", t, vecs[i], metadata={"source": f"doc{i}"})

    q = "programming and machine learning"
    qv = emb.embed([q])[0]
    results = store.search(qv, top_k=3)
    assert len(results) > 0
    # best match should be the Python doc (doc2)
    best_score, best_item = results[0]
    assert best_item["id"] == "doc2"
