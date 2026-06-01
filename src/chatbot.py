import argparse
import sys

from src.core.provider_factory import create_provider
from src.telemetry.logger import logger
from src.telemetry.metrics import tracker


SYSTEM_PROMPT = (
    "You are a concise, helpful AI lab chatbot. "
    "Answer clearly, ask follow-up questions only when necessary, and keep responses practical."
)


class Chatbot:
    """
    Minimal chatbot baseline for comparison with the VinWonders RAG API.
    """

    def __init__(self):
        self.provider = create_provider()
        self.history: list[tuple[str, str]] = []

    def ask(self, user_input: str) -> str:
        prompt = self._build_prompt(user_input)
        logger.log_event(
            "CHATBOT_REQUEST",
            {"provider": self.provider.__class__.__name__, "model": self.provider.model_name},
        )

        result = self.provider.generate(prompt, system_prompt=SYSTEM_PROMPT)
        answer = result["content"].strip()
        self.history.append((user_input, answer))

        tracker.track_request(
            provider=result["provider"],
            model=self.provider.model_name,
            usage=result["usage"],
            latency_ms=result["latency_ms"],
        )
        return answer

    def _build_prompt(self, user_input: str) -> str:
        if not self.history:
            return user_input

        turns = [f"User: {user}\nAssistant: {assistant}" for user, assistant in self.history[-5:]]
        turns.append(f"User: {user_input}\nAssistant:")
        return "\n\n".join(turns)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Lab 3 chatbot baseline.")
    parser.add_argument("--message", "-m", help="Send one message and exit.")
    args = parser.parse_args()

    bot = Chatbot()
    if args.message:
        print(bot.ask(args.message))
        return 0

    print(f"Chatbot ready ({bot.provider.__class__.__name__}, model={bot.provider.model_name})")
    print("Type 'exit' or 'quit' to stop.")
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if user_input.lower() in {"exit", "quit"}:
            return 0
        if not user_input:
            continue

        try:
            print(f"Assistant: {bot.ask(user_input)}")
        except Exception as exc:
            logger.error(f"Chatbot request failed: {exc}")
            print(f"Error: {exc}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
