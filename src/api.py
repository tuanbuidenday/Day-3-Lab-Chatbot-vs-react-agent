import os
from typing import Dict, List, Optional
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.core.provider_factory import create_provider
from src.rag.retriever import RetrievedDocument, VinWondersRetriever
from src.telemetry.logger import logger
from src.telemetry.metrics import tracker


load_dotenv()

app = FastAPI(
    title="VinWonders Chatbot API",
    description="Local demo backend for a VinWonders virtual travel guide chatbot.",
    version="1.0.0",
)

retriever = VinWondersRetriever()
conversation_store: Dict[str, List[Dict[str, str]]] = {}


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    location: Optional[str] = Field(
        default=None,
        description="Optional VinWonders location filter, e.g. Phu Quoc, Nha Trang, Ha Noi.",
    )
    max_context_docs: int = Field(default=4, ge=1, le=8)


class SourceDocument(BaseModel):
    id: str
    title: str
    category: str
    location: Optional[str] = None
    zone: Optional[str] = None
    score: float


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[SourceDocument]
    provider: str
    model: str
    latency_ms: int
    usage: Dict[str, int]


class SearchResponse(BaseModel):
    query: str
    results: List[dict]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": os.getenv("DEFAULT_PROVIDER", "ollama"),
        "model": os.getenv("DEFAULT_MODEL", "llama3"),
    }


@app.get("/knowledge/search", response_model=SearchResponse)
def search_knowledge(
    q: str,
    location: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 4,
):
    documents = retriever.search(q, location=location, category=category, limit=limit)
    return {
        "query": q,
        "results": [document.to_dict() for document in documents],
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid4())
    history = conversation_store.setdefault(session_id, [])
    sources = retriever.search(
        request.message,
        location=request.location,
        limit=request.max_context_docs,
    )
    if not sources:
        sources = retriever.search("tong quan vinwonders", limit=request.max_context_docs)

    provider = create_provider()
    prompt = _build_prompt(request.message, history, sources)

    try:
        result = provider.generate(prompt, system_prompt=_system_prompt())
    except Exception as exc:
        logger.error(f"VinWonders chatbot failed: {exc}")
        raise HTTPException(status_code=503, detail=f"LLM provider unavailable: {exc}") from exc

    answer = result["content"].strip()
    history.extend(
        [
            {"role": "user", "content": request.message},
            {"role": "assistant", "content": answer},
        ]
    )
    conversation_store[session_id] = history[-10:]

    tracker.track_request(
        provider=result["provider"],
        model=provider.model_name,
        usage=result["usage"],
        latency_ms=result["latency_ms"],
    )
    logger.log_event(
        "VINWONDERS_CHAT",
        {
            "session_id": session_id,
            "source_ids": [source.id for source in sources],
            "latency_ms": result["latency_ms"],
        },
    )

    return ChatResponse(
        session_id=session_id,
        answer=answer,
        sources=[_source_document(source) for source in sources],
        provider=result["provider"],
        model=provider.model_name,
        latency_ms=result["latency_ms"],
        usage=result["usage"],
    )


def _system_prompt() -> str:
    return (
        "Bạn là hướng dẫn viên du lịch ảo của VinWonders Việt Nam. "
        "Trả lời bằng tiếng Việt tự nhiên, ngắn gọn, ưu tiên thông tin trong CONTEXT. "
        "Nếu dữ liệu không có thông tin chắc chắn, hãy nói rõ là chưa có trong dữ liệu demo. "
        "Luôn hữu ích với du khách: gợi ý khu vực, thời gian tham quan, lưu ý an toàn và dịch vụ liên quan."
    )


def _build_prompt(
    message: str,
    history: List[Dict[str, str]],
    sources: List[RetrievedDocument],
) -> str:
    context = retriever.build_context(sources)
    recent_history = "\n".join(
        f"{turn['role'].title()}: {turn['content']}" for turn in history[-6:]
    )
    if not recent_history:
        recent_history = "No previous conversation."

    return f"""
CONTEXT:
{context}

RECENT CONVERSATION:
{recent_history}

USER QUESTION:
{message}

INSTRUCTIONS:
- Dựa vào CONTEXT để trả lời.
- Nếu câu hỏi xin lịch trình, hãy đề xuất lịch trình theo mốc thời gian.
- Nếu câu hỏi về trò chơi cảm giác mạnh, nhắc điều kiện chiều cao/tuổi/sức khỏe nếu có trong dữ liệu.
- Kết thúc bằng 1 gợi ý bước tiếp theo phù hợp.
"""


def _source_document(document: RetrievedDocument) -> SourceDocument:
    return SourceDocument(
        id=document.id,
        title=document.title,
        category=document.category,
        location=document.location,
        zone=document.zone,
        score=document.score,
    )
