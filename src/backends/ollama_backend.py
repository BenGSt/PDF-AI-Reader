from .base import BackendBase


class OllamaBackend(BackendBase):
    """Stub Ollama backend client for local Ollama HTTP API.
    This is intentionally a stub: full implementation should handle HTTP requests and streaming.
    """

    def __init__(self, url: str = "http://localhost:11434"):
        self.url = url

    async def generate(self, prompt: str, **kwargs):
        raise NotImplementedError("Ollama client not implemented in scaffold")
