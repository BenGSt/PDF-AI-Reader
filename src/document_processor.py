"""Minimal document loader for TXT/MD/PDF that returns plain text.
This is a lightweight scaffold: robust extraction can be added later.
"""
from pathlib import Path


def load_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    suffix = p.suffix.lower().lstrip('.')
    if suffix in ("txt", "md"):
        return p.read_text(encoding="utf-8")

    if suffix == "pdf":
        try:
            import fitz  # PyMuPDF

            doc = fitz.open(str(p))
            text_parts = []
            for page in doc:
                text_parts.append(page.get_text())
            return "\n".join(text_parts)
        except Exception:
            # Fall back to empty string if PyMuPDF isn't available in the environment
            return ""

    # For unknown types return empty string for now
    return ""
