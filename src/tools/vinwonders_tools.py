import json
from typing import Any, Callable, Dict, List

from src.rag.retriever import VinWondersRetriever
from src.security.guardrails import ChatGuardrails


ToolFunction = Callable[[str], str]


class VinWondersTools:
    """
    Tool inventory used by the ReAct agents.
    """

    def __init__(self):
        self.retriever = VinWondersRetriever()
        self.guardrails = ChatGuardrails()

    def definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "search_knowledge",
                "description": (
                    "Search VinWonders attractions, zones, services, FAQs, prices, and schedules. "
                    "Input can be plain text or JSON: {'query': str, 'location': str optional, 'limit': int optional}."
                ),
                "function": self.search_knowledge,
            },
            {
                "name": "suggest_itinerary",
                "description": (
                    "Suggest a visit itinerary. Input can be plain text or JSON: "
                    "{'location': str optional, 'audience': str optional}."
                ),
                "function": self.suggest_itinerary,
            },
            {
                "name": "safety_check",
                "description": (
                    "Return safety and preparation notes for a ride, zone, or visitor profile. "
                    "Input can be plain text or JSON: {'activity': str}."
                ),
                "function": self.safety_check,
            },
        ]

    def search_knowledge(self, raw_args: str) -> str:
        args = self._parse_args(raw_args)
        query = args.get("query") or raw_args
        location = args.get("location")
        limit = min(int(args.get("limit", 3) or 3), 5)

        guardrail_result = self.guardrails.validate_search(query, limit)
        if not guardrail_result.allowed:
            return guardrail_result.safe_response

        results = self.retriever.search(query, location=location, limit=limit)
        if not results:
            return "Không tìm thấy thông tin phù hợp trong dữ liệu VinWonders demo."

        return "\n\n".join(
            f"- {doc.title} [{doc.category}]: {doc.content.strip()[:650]}"
            for doc in results
        )

    def suggest_itinerary(self, raw_args: str) -> str:
        args = self._parse_args(raw_args)
        location = args.get("location") or self._infer_location(raw_args)
        audience = args.get("audience", "")
        query = f"lich trinh {location} {audience}".strip()
        results = self.retriever.search(query, location=location, category="itinerary", limit=2)
        if not results:
            results = self.retriever.search(query or "lich trinh vinwonders", limit=3)
        return "\n\n".join(f"- {doc.title}: {doc.content.strip()[:900]}" for doc in results)

    def safety_check(self, raw_args: str) -> str:
        args = self._parse_args(raw_args)
        activity = args.get("activity") or args.get("query") or raw_args
        results = self.retriever.search(f"luu y suc khoe an toan {activity}", limit=3)
        notes = [
            "Người cao huyết áp, tim mạch, phụ nữ mang thai nên tránh trò chơi cảm giác mạnh.",
            "Nên đi giày thoải mái, mang kem chống nắng và uống đủ nước.",
        ]
        notes.extend(f"{doc.title}: {doc.content.strip()[:500]}" for doc in results)
        return "\n\n".join(notes)

    def _parse_args(self, raw_args: str) -> Dict[str, Any]:
        try:
            parsed = json.loads(raw_args)
        except (TypeError, json.JSONDecodeError):
            return {}
        return parsed if isinstance(parsed, dict) else {}

    def _infer_location(self, text: str) -> str:
        normalized = text.lower()
        if "phú quốc" in normalized or "phu quoc" in normalized:
            return "Phú Quốc"
        if "nha trang" in normalized:
            return "Nha Trang"
        if "hội an" in normalized or "hoi an" in normalized:
            return "Nam Hội An"
        if "hà nội" in normalized or "ha noi" in normalized:
            return "Hà Nội"
        return ""
