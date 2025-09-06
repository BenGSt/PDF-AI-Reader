class BackendBase:
    """Abstract LLM backend interface for the scaffold."""

    async def generate(self, prompt: str, **kwargs):
        raise NotImplementedError()
