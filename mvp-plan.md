# MVP Plan — Document Chat (Offline-first)

Goal
- Deliver a minimal, offline-first document chat that reliably runs on macOS Apple Silicon (M-series) and on CPU-only systems.

Scope (what this MVP must include)
- PDF + Markdown + plain-text ingestion
- Semantic chunking with configurable overlap
- Local embeddings using sentence-transformers (CPU-capable)
- ChromaDB vector store with Top-K retrieval
- Ollama backend integration for macOS (llama.cpp CPU fallback)
- Minimal CLI: add, list, remove, start, ask
- Source citation in responses

High-level checklist (implementation order)
1. Project scaffolding
   - create `src/` skeleton if missing
   - add `requirements/base.txt` with core deps
2. Platform detector
   - implement `src/platform_detector.py` (macOS/CPU detection)
3. Document loaders & chunker
   - implement `src/document_processor.py` with PyMuPDF and markdown loader
   - add semantic chunker with overlap config
4. Embeddings
   - implement `src/embeddings.py` using sentence-transformers (CPU fallback)
   - caching layer for embeddings
5. Vector store
   - implement `src/vector_store.py` to wrap ChromaDB storage and Top-K search
6. LLM backend
   - implement `src/backends/ollama_backend.py` (HTTP client) and `llamacpp` fallback stub
7. CLI
   - add `src/cli.py` with commands: --add, --list, --remove, --start, --ask
8. Tests & smoke checks
   - `tests/test_smoke_index.py` (index a small PDF)
   - `tests/test_smoke_query.py` (ask a simple question and assert non-empty answer + sources)
9. Docs
   - add `docs/mvp-readme.md` with quick start and sample commands

Acceptance criteria (definition of done)
- End-to-end: add document -> index -> ask -> answer with sources works offline on M-series
- Index a 100-page PDF within a single run (empirical target)
- Basic smoke tests pass locally

Files to create/update (minimal)
- `mvp-plan.md` (this file)
- `src/platform_detector.py`
- `src/document_processor.py`
- `src/embeddings.py`
- `src/vector_store.py`
- `src/backends/ollama_backend.py`
- `src/cli.py`
- `requirements/base.txt`
- `tests/test_smoke_index.py`

Quick "try it" (after implementation)

```bash
# install deps
python -m pip install -r requirements/base.txt

# add a document and start an interactive session
python -m src.cli --add docs/sample.pdf
python -m src.cli --start

# one-shot query
python -m src.cli --query "What are the main conclusions?"
```

Next steps I can take for you
- Scaffold the `src/` modules and a minimal `requirements/base.txt` and smoke tests now.
- Or, if you prefer, I can implement the platform detector and document processor first.

Pick one (scaffold all files vs implement a subset) and I'll proceed.
