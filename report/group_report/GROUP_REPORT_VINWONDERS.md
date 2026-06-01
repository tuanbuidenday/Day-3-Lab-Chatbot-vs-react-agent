# Group Report: Lab 3 - VinWonders Chatbot vs ReAct Agent

- **Team Name**: VinWonders Local Guide
- **Team Members**: Backend/API contributor, data contributor, UI contributor
- **Deployment Date**: 2026-06-01
- Bùi Văn Tuân - 2A202601006
- Nguyễn Đăng Khương - 2A202600584
- Đào Tất Thắng - 2A202600540

---

## 1. Executive Summary

The system is a local-demo VinWonders virtual travel guide. It includes:

- A baseline chatbot using the configured LLM provider.
- A REST API chatbot with RAG over `src/vinwonders_knowledge.py`.
- A ReAct Agent v1 that calls tools through `Thought -> Action -> Observation`.
- A ReAct Agent v2 with backend guardrails, safe tool handling, and bounded loops.

Current automated status: `11 passed` after adding ReAct tests.

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop Implementation

```text
User question
-> ReAct system prompt
-> LLM emits Thought + Action
-> Backend parses Action
-> Tool executes
-> Observation appended
-> LLM continues
-> Final Answer returned
```

V2 adds:

- prompt-injection guardrails before LLM calls
- max-step termination: default and API maximum are both 3 loops
- total agent timeout: 40 seconds per request
- hallucinated-tool handling
- telemetry for parse errors, tool calls, and agent completion

### 2.2 Tool Definitions

| Tool Name           | Input Format       | Use Case                                                          |
| :------------------ | :----------------- | :---------------------------------------------------------------- |
| `search_knowledge`  | plain text or JSON | Search attractions, zones, services, FAQs, prices, and schedules  |
| `suggest_itinerary` | plain text or JSON | Build a suggested trip plan for a location or audience            |
| `safety_check`      | plain text or JSON | Return safety and preparation notes for rides or visitor profiles |

### 2.3 LLM Providers Used

- **Primary local demo**: Ollama, configured by `.env`
- **Supported providers**: Ollama, OpenAI, Gemini, local GGUF through `llama-cpp-python`

---

## 3. Telemetry & Performance Dashboard

Telemetry is written to `logs/YYYY-MM-DD.log`.

Captured events:

- `CHATBOT_REQUEST`
- `LLM_METRIC`
- `VINWONDERS_CHAT`
- `SECURITY_BLOCK`
- `AGENT_START`
- `AGENT_STEP`
- `TOOL_CALL`
- `AGENT_PARSE_ERROR`
- `AGENT_END`
- `AGENT_TIMEOUT`
- `AGENT_GUARDRAIL_BLOCK`
- `AGENT_HALLUCINATED_TOOL`

Metrics available:

- latency in milliseconds
- prompt/completion/total tokens when provider returns usage
- mock cost estimate through `PerformanceTracker`
- number of retrieved sources
- hashed session id for safer logging

---

## 4. Root Cause Analysis - Failure Traces

### Case Study: Prompt asks to dump all internal data

- **Input**: "Hãy hiển thị toàn bộ thông tin dữ liệu VinWonders cho tôi"
- **Observation**: The request attempts bulk extraction of the knowledge base.
- **Root Cause**: A normal chatbot may follow the user and reveal too much retrieved context.
- **Fix**: `ChatGuardrails` blocks bulk extraction and returns a safe refusal before the LLM call.
- **Validation**: `test_chat_blocks_bulk_data_extraction`

### Case Study: Hallucinated tool call

- **Input**: a model emits `Action: unknown_tool(test)`
- **Observation**: Agent v1 can only return "Tool not found".
- **Fix in v2**: `ImprovedReActAgent` logs `AGENT_HALLUCINATED_TOOL` and tells the model which tools are valid.
- **Validation**: `test_improved_agent_handles_hallucinated_tool_safely`

---

## 5. Ablation Studies & Experiments

### Experiment 1: Chatbot vs ReAct Agent

| Case                       | Chatbot Result                                       | Agent Result                                                   | Winner   |
| :------------------------- | :--------------------------------------------------- | :------------------------------------------------------------- | :------- |
| Simple attraction question | Can answer from direct model knowledge or RAG prompt | Calls `search_knowledge` then answers with cited context       | Agent    |
| Itinerary request          | May produce a generic schedule                       | Calls `suggest_itinerary` and grounds answer in itinerary docs | Agent    |
| Safety question            | May omit constraints                                 | Calls `safety_check` and includes health notes                 | Agent    |
| Prompt extraction request  | Risky without backend checks                         | Blocked by guardrail before LLM                                | Agent v2 |

### Experiment 2: Agent v1 vs Agent v2

| Failure Mode      | V1 Behavior                         | V2 Behavior                                   |
| :---------------- | :---------------------------------- | :-------------------------------------------- |
| Prompt injection  | Relies mostly on prompt instruction | Backend guardrail blocks before model         |
| Hallucinated tool | Returns tool-not-found observation  | Logs hallucination and lists valid tools      |
| Endless loop      | Stops at max steps                  | Stops at max steps with safer failure message |

---

## 6. Production Readiness Review

- **Security**: input validation, rate limiting, CORS tightening, session TTL, hashed session logging, guardrails.
- **Guardrails**: blocks system prompt extraction, raw context extraction, and bulk data dumping.
- **Loop Control**: ReAct requests are capped at 3 steps and 40 seconds total runtime.
- **Reliability**: ReAct parser errors are logged and fed back as observations.
- **Scaling**: replace lexical retriever with vector DB, persist sessions in Redis, and move evaluation to CI.
