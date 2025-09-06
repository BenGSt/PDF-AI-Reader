PDF-AI-Reader
===============

Quick start (Python 3.11)

This project targets Python 3.11+. The repository includes a `.python-version` file for `pyenv` users.

Create a project virtualenv and install test deps:

```bash
cd /Users/bengst/Documents/ClaudeDesktop/PDF-AI-Reader
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements/test.txt
pytest -q tests/smoke
```

Install full development environment (heavy; includes ML packages):

```bash
# with venv activated
python -m pip install -r requirements/base.txt
```

Notes
- If you use `pyenv`, run `pyenv install 3.11.6` then `pyenv local 3.11.6` before creating the venv.
- The smoke tests are lightweight and will run without heavy ML models (the scaffold falls back to simple embeddings when models are not available).
