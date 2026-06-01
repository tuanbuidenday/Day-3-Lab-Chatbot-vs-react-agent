from typing import Any, Dict, List

from src.agent.agent import ReActAgent
from src.core.llm_provider import LLMProvider
from src.security.guardrails import SAFE_REFUSAL, ChatGuardrails
from src.telemetry.logger import logger


class ImprovedReActAgent(ReActAgent):
    """
    V2 agent with backend guardrails and deterministic fallback when the LLM
    fails to produce a valid ReAct action.
    """

    def __init__(
        self,
        llm: LLMProvider,
        tools: List[Dict[str, Any]],
        max_steps: int = 3,
        timeout_seconds: int = 40,
    ):
        super().__init__(
            llm=llm,
            tools=tools,
            max_steps=max_steps,
            timeout_seconds=timeout_seconds,
        )
        self.guardrails = ChatGuardrails()

    def run(self, user_input: str) -> str:
        guardrail_result = self.guardrails.validate_message(user_input)
        if not guardrail_result.allowed:
            logger.log_event("AGENT_GUARDRAIL_BLOCK", {"reason": guardrail_result.reason})
            return guardrail_result.safe_response or SAFE_REFUSAL
        return super().run(user_input)

    def _execute_tool(self, tool_name: str, args: str) -> str:
        if tool_name not in {tool["name"] for tool in self.tools}:
            logger.log_event("AGENT_HALLUCINATED_TOOL", {"tool": tool_name})
            return (
                f"Tool {tool_name} không tồn tại. "
                "Hãy dùng một trong các tool hợp lệ: "
                + ", ".join(tool["name"] for tool in self.tools)
            )
        return super()._execute_tool(tool_name, args)
