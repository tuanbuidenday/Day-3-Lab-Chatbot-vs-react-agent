from dataclasses import dataclass
from typing import List

from src.agent.improved_agent import ImprovedReActAgent
from src.core.provider_factory import create_provider
from src.rag.retriever import VinWondersRetriever
from src.tools.vinwonders_tools import VinWondersTools


@dataclass
class EvaluationCase:
    query: str
    expected_terms: List[str]


CASES = [
    EvaluationCase("Gợi ý lịch trình 1 ngày ở VinWonders Phú Quốc", ["Phú Quốc", "Water World"]),
    EvaluationCase("Trẻ nhỏ nên đi khu nào ở VinWonders?", ["trẻ", "Ocean"]),
    EvaluationCase("Có lưu ý an toàn nào khi chơi trò cảm giác mạnh?", ["tim mạch", "phụ nữ mang thai"]),
    EvaluationCase("Ở Nha Trang có vườn thú không?", ["Nha Trang", "vườn thú"]),
]


def run_keyword_eval() -> None:
    retriever = VinWondersRetriever()
    tools = VinWondersTools().definitions()
    agent = ImprovedReActAgent(create_provider(), tools, max_steps=4)

    print("| Case | Retriever Hit | Agent Answer Preview |")
    print("| :--- | :---: | :--- |")
    for case in CASES:
        docs = retriever.search(case.query, limit=4)
        context = " ".join(doc.content + " " + doc.title for doc in docs).lower()
        hit = all(term.lower() in context for term in case.expected_terms)
        answer = agent.run(case.query).replace("\n", " ")[:160]
        print(f"| {case.query} | {'yes' if hit else 'no'} | {answer} |")


if __name__ == "__main__":
    run_keyword_eval()
