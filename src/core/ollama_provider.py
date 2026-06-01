import json
import time
from typing import Any, Dict, Generator, Optional

import requests

from src.core.llm_provider import LLMProvider


class OllamaProvider(LLMProvider):
    """
    Provider for self-hosted open-source models served by Ollama.
    """

    def __init__(
        self,
        model_name: str = "llama3",
        api_key: Optional[str] = None,
        base_url: str = "http://localhost:11434",
        timeout: int = 120,
    ):
        super().__init__(model_name, api_key)
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        start_time = time.time()
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=self._build_payload(prompt, system_prompt, stream=False),
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()

        latency_ms = int((time.time() - start_time) * 1000)
        usage = self._extract_usage(data)
        return {
            "content": data.get("response", ""),
            "usage": usage,
            "latency_ms": latency_ms,
            "provider": "ollama",
        }

    def stream(self, prompt: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        with requests.post(
            f"{self.base_url}/api/generate",
            json=self._build_payload(prompt, system_prompt, stream=True),
            timeout=self.timeout,
            stream=True,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                if token:
                    yield token

    def _build_payload(self, prompt: str, system_prompt: Optional[str], stream: bool) -> Dict[str, Any]:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": stream,
        }
        if system_prompt:
            payload["system"] = system_prompt
        return payload

    def _extract_usage(self, data: Dict[str, Any]) -> Dict[str, int]:
        prompt_tokens = int(data.get("prompt_eval_count", 0) or 0)
        completion_tokens = int(data.get("eval_count", 0) or 0)
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        }
