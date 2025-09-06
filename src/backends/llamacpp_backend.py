from .base import BackendBase


class LlamaCppBackend(BackendBase):
    """Stub llama.cpp backend for scaffold. Implement platform-specific binary bindings later."""

    def __init__(self, binary_path: str = None):
        self.binary_path = binary_path

    async def generate(self, prompt: str, **kwargs):
        raise NotImplementedError("llama.cpp client not implemented in scaffold")
