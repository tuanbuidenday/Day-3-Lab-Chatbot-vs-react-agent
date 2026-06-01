import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from src.vinwonders_knowledge import VINWONDERS_DOCUMENTS


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "at",
    "co",
    "cua",
    "duoc",
    "gi",
    "giup",
    "hoi",
    "la",
    "mot",
    "nhung",
    "tai",
    "the",
    "thi",
    "toi",
    "trong",
    "ve",
    "vinwonders",
    "vui",
    "what",
    "where",
    "which",
    "with",
}


@dataclass
class RetrievedDocument:
    id: str
    title: str
    content: str
    category: str
    location: Optional[str]
    zone: Optional[str]
    score: float

    def to_dict(self, max_content_chars: int = 800) -> Dict[str, Any]:
        content = self.content.strip()
        if len(content) > max_content_chars:
            content = f"{content[:max_content_chars].rstrip()}..."

        return {
            "id": self.id,
            "title": self.title,
            "content": content,
            "category": self.category,
            "location": self.location,
            "zone": self.zone,
            "score": self.score,
        }


class VinWondersRetriever:
    """
    Lightweight lexical retriever optimized for local demos.
    """

    def __init__(self, documents: Optional[Iterable[Dict[str, Any]]] = None):
        self.documents = list(documents or VINWONDERS_DOCUMENTS)
        self._indexed = [
            {
                "raw": document,
                "tokens": self._tokenize(
                    " ".join(
                        [
                            document.get("title", ""),
                            document.get("category", ""),
                            document.get("location", ""),
                            document.get("zone", ""),
                            document.get("content", ""),
                        ]
                    )
                ),
            }
            for document in self.documents
        ]

    def search(
        self,
        query: str,
        location: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 4,
    ) -> List[RetrievedDocument]:
        query_tokens = self._tokenize(query)
        if location:
            query_tokens.update(self._tokenize(location))

        results: List[RetrievedDocument] = []
        for item in self._indexed:
            document = item["raw"]
            if location and location.lower() not in document.get("location", "").lower():
                if document.get("location"):
                    continue
            if category and category.lower() != document.get("category", "").lower():
                continue

            score = self._score(query_tokens, item["tokens"], document, location)
            if score <= 0:
                continue

            results.append(
                RetrievedDocument(
                    id=document["id"],
                    title=document["title"],
                    content=document["content"],
                    category=document.get("category", ""),
                    location=document.get("location"),
                    zone=document.get("zone"),
                    score=round(score, 3),
                )
            )

        results.sort(key=lambda doc: doc.score, reverse=True)
        return results[: max(1, limit)]

    def build_context(self, documents: List[RetrievedDocument]) -> str:
        chunks = []
        for index, document in enumerate(documents, start=1):
            location = f" | Location: {document.location}" if document.location else ""
            zone = f" | Zone: {document.zone}" if document.zone else ""
            chunks.append(
                f"[{index}] {document.title} ({document.category}{location}{zone})\n"
                f"{document.content.strip()}"
            )
        return "\n\n".join(chunks)

    def _score(
        self,
        query_tokens: set[str],
        document_tokens: set[str],
        document: Dict[str, Any],
        location: Optional[str],
    ) -> float:
        overlap = query_tokens.intersection(document_tokens)
        score = float(len(overlap))

        title_tokens = self._tokenize(document.get("title", ""))
        score += len(query_tokens.intersection(title_tokens)) * 1.5

        if location and location.lower() in document.get("location", "").lower():
            score += 3

        if document.get("category") == "itinerary" and query_tokens.intersection(
            {"lich", "trinh", "goi", "goi-y", "tham", "quan", "schedule", "itinerary"}
        ):
            score += 2

        return score

    def _tokenize(self, text: str) -> set[str]:
        normalized = text.lower().replace("đ", "d")
        tokens = set(re.findall(r"[a-z0-9]+", normalized))
        return {token for token in tokens if len(token) > 1 and token not in STOPWORDS}
