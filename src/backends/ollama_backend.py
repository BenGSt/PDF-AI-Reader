from .base import BackendBase
import asyncio


class OllamaBackend(BackendBase):
    """Basic Ollama backend client for local Ollama HTTP API."""

    def __init__(self, url: str = "http://localhost:11434", model: str = "gemma3"):
        self.url = url
        self.model = model
        self.available = False
        # Check if Ollama is available
        try:
            import aiohttp
            self.session = None
            self.available = True
        except ImportError:
            self.available = False

    async def _ensure_session(self):
        if not self.available:
            return False
        if self.session is None:
            try:
                import aiohttp
                self.session = aiohttp.ClientSession()
            except Exception:
                self.available = False
                return False
        return True

    async def generate(self, prompt: str, **kwargs):
        if not await self._ensure_session():
            return f"[OLLAMA UNAVAILABLE] {prompt[:100]}..."

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
            async with self.session.post(f"{self.url}/api/generate", json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "[NO RESPONSE]")
                else:
                    return f"[OLLAMA ERROR {response.status}] {await response.text()}"
        except Exception as e:
            return f"[OLLAMA ERROR] {str(e)}"
        finally:
            if self.session:
                await self.session.close()
                self.session = None

    async def close(self):
        if self.session:
            await self.session.close()
