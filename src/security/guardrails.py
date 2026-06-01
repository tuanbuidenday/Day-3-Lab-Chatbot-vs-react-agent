import re
import unicodedata
from dataclasses import dataclass


SAFE_REFUSAL = (
    "Mình không thể hiển thị toàn bộ dữ liệu nội bộ, system prompt hoặc context thô. "
    "Bạn có thể hỏi cụ thể về địa điểm, trò chơi, dịch vụ hoặc lịch trình VinWonders, "
    "mình sẽ tóm tắt thông tin phù hợp."
)


@dataclass
class GuardrailResult:
    allowed: bool
    reason: str = ""
    safe_response: str = ""


class ChatGuardrails:
    """
    Backend-side guardrails for prompt injection and bulk data extraction.
    """

    BLOCK_PATTERNS = [
        r"\b(ignore|bypass|override|forget)\b.*\b(system|instruction|previous|guardrail|policy)\b",
        r"\b(show|print|reveal|display|dump|export|return)\b.*\b(system prompt|developer prompt|prompt|context|raw|database|knowledge base|all data|all documents)\b",
        r"\b(hien|hien thi|in|xuat|tra|show|dump)\b.*\b(toan bo|tat ca|du lieu|thong tin|context|prompt|he thong)\b",
        r"\b(prompt injection|jailbreak|roleplay as system|act as system)\b",
        r"\bVINWONDERS_DOCUMENTS\b",
    ]

    BULK_EXTRACTION_PATTERNS = [
        r"\b(tat ca|toan bo|full|entire|complete)\b.*\b(vinwonders|tro choi|dich vu|tai lieu|document|data|thong tin)\b",
        r"\b(list|liet ke|ke het)\b.*\b(tat ca|toan bo|full|entire)\b",
    ]

    def validate_message(self, message: str) -> GuardrailResult:
        normalized = self._normalize(message)

        if len(message) > 2000:
            return GuardrailResult(False, "message_too_long", SAFE_REFUSAL)

        for pattern in self.BLOCK_PATTERNS:
            if re.search(pattern, normalized):
                return GuardrailResult(False, "prompt_or_context_extraction", SAFE_REFUSAL)

        for pattern in self.BULK_EXTRACTION_PATTERNS:
            if re.search(pattern, normalized):
                return GuardrailResult(False, "bulk_data_extraction", SAFE_REFUSAL)

        return GuardrailResult(True)

    def validate_search(self, query: str, limit: int) -> GuardrailResult:
        normalized = self._normalize(query)
        if limit > 5:
            return GuardrailResult(False, "search_limit_exceeded", SAFE_REFUSAL)

        for pattern in self.BLOCK_PATTERNS + self.BULK_EXTRACTION_PATTERNS:
            if re.search(pattern, normalized):
                return GuardrailResult(False, "unsafe_search_query", SAFE_REFUSAL)

        return GuardrailResult(True)

    def _normalize(self, text: str) -> str:
        text = text.lower().replace("đ", "d")
        return "".join(
            char for char in unicodedata.normalize("NFD", text) if unicodedata.category(char) != "Mn"
        )
