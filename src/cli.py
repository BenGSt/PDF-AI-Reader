"""Minimal CLI to add documents and query the in-memory store for MVP scaffolding.
This is intentionally simple and sync to keep the scaffold easy to run.
"""
import argparse
import uuid
from pathlib import Path

from . import __version__
from .document_processor import load_text
from .embeddings import Embeddings
from .vector_store import get_default_store


EMB = Embeddings()
STORE = get_default_store()


def cmd_add(paths):
    for p in paths:
        p = Path(p)
        if not p.exists():
            print(f"file not found: {p}")
            continue
        try:
            text = load_text(str(p))
        except Exception as e:
            print(f"error loading {p}: {e}")
            continue
        vec = EMB.embed([text])[0]
        doc_id = str(uuid.uuid4())
        STORE.add(doc_id, text, vec, metadata={"source": str(p)})
        print(f"indexed: {p} -> id={doc_id}")


def cmd_query(q, k=3):
    vec = EMB.embed([q])[0]
    results = STORE.search(vec, top_k=k)
    for score, item in results:
        print(f"score={score:.4f} source={item.get('metadata', {}).get('source')} id={item.get('id')}")
        snippet = item.get("text", "")[:400].replace("\n", " ")
        print(f"  snippet: {snippet}\n")


def main():
    parser = argparse.ArgumentParser(prog="doc-chat")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--add", nargs="*", help="add documents to the knowledge base")
    parser.add_argument("--query", help="one-shot query")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        return

    if args.add:
        cmd_add(args.add)
        return

    if args.query:
        cmd_query(args.query)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
