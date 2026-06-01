import os

from dotenv import load_dotenv


def create_provider():
    """
    Build an LLM provider from .env settings.
    """
    load_dotenv()

    provider = os.getenv("DEFAULT_PROVIDER", "ollama").lower()
    model = os.getenv("DEFAULT_MODEL", "llama3")

    if provider == "ollama":
        from src.core.ollama_provider import OllamaProvider

        return OllamaProvider(
            model_name=model,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    if provider == "openai":
        from src.core.openai_provider import OpenAIProvider

        return OpenAIProvider(
            model_name=model,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    if provider in {"google", "gemini"}:
        from src.core.gemini_provider import GeminiProvider

        return GeminiProvider(
            model_name=model,
            api_key=os.getenv("GEMINI_API_KEY"),
        )

    if provider == "local":
        from src.core.local_provider import LocalProvider

        return LocalProvider(
            model_path=os.getenv("LOCAL_MODEL_PATH", "./models/Phi-3-mini-4k-instruct-q4.gguf"),
        )

    raise ValueError(
        f"Unsupported DEFAULT_PROVIDER={provider}. "
        "Use one of: ollama, openai, google, gemini, local."
    )
