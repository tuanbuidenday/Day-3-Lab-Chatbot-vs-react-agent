from fastapi.testclient import TestClient

from src.api import app
from src.rag.retriever import VinWondersRetriever


def test_retriever_finds_phu_quoc_water_world():
    retriever = VinWondersRetriever()

    results = retriever.search("tro choi nuoc phu quoc", location="Phú Quốc", limit=3)

    assert results
    assert any("Thế giới Nước" in result.title for result in results)


def test_search_endpoint_returns_sources():
    client = TestClient(app)

    response = client.get("/knowledge/search", params={"q": "lich trinh nha trang", "limit": 2})

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "lich trinh nha trang"
    assert len(data["results"]) > 0
    assert {"id", "title", "content", "category", "score"}.issubset(data["results"][0])


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
