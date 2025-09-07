"""Tiny cross-platform TTS helper used by the CLI.

On macOS this prefers the builtin `say` command. On other platforms it will try
to use `pyttsx3` if available. The function returns True on success and False on
failure.
"""
from typing import Optional
import platform
import subprocess


def speak(text: str, _max_chars: int = 2000) -> bool:
    """Speak the given text using a best-effort backend.

    Returns True if the text was sent to a TTS backend successfully, False
    otherwise.
    """
    if not text:
        return False

    if len(text) > _max_chars:
        text = text[:_max_chars] + "..."

    system = platform.system()
    # macOS has a reliable 'say' binary
    if system == "Darwin":
        try:
            subprocess.run(["say", text], check=True)
            return True
        except Exception:
            return False

    # Try pyttsx3 as a pure-Python fallback (cross-platform)
    try:
        import pyttsx3

        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception:
        return False


__all__ = ["speak"]
