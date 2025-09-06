import os
from src.document_processor import load_text
from src.embeddings import Embeddings
from src.vector_store import SimpleVectorStore


def test_index_and_search(tmp_path):
    # create a small text file
    p = tmp_path / "sample.txt"
    p.write_text("This is a short test document about AI and machine learning.")

    text = load_text(str(p))
    assert "test document" in text

    emb = Embeddings()
    vec = emb.embed([text])[0]

    store = SimpleVectorStore()
    store.add("doc1", text, vec, metadata={"source": str(p)})

    results = store.search(vec, top_k=1)
    assert len(results) == 1
    score, item = results[0]
    assert score > 0.0
    assert item["metadata"]["source"] == str(p)
