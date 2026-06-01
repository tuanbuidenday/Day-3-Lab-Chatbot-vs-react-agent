# Lab 3: Chatbot vs ReAct Agent (Industry Edition)

Welcome to Phase 3 of the Agentic AI course! This lab focuses on moving from a simple LLM Chatbot to a sophisticated **ReAct Agent** with industry-standard monitoring.

## 🚀 Getting Started

### 1. Setup Environment
Copy the `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

By default the demo backend can use Ollama on your machine:
```env
DEFAULT_PROVIDER=ollama
DEFAULT_MODEL=llama3
OLLAMA_BASE_URL=http://localhost:11434
```

Make sure Ollama is running and the model exists locally:
```bash
ollama pull llama3
ollama serve
```

### 3. Run the VinWonders Backend API
Start the REST API:
```bash
python3 -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8000
```

Open API docs:
```text
http://127.0.0.1:8000/docs
```

Search the local VinWonders knowledge base:
```bash
curl "http://127.0.0.1:8000/knowledge/search?q=lich%20trinh%20phu%20quoc&limit=3"
```

Ask the RAG chatbot:
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"Gợi ý lịch trình 1 ngày ở VinWonders Phú Quốc","location":"Phú Quốc"}'
```

Ask the ReAct Agent v2 with tools:
```bash
curl -X POST "http://127.0.0.1:8000/agent/react" \
  -H "Content-Type: application/json" \
  -d '{"message":"Kiểm tra an toàn và gợi ý lịch trình cho gia đình ở Phú Quốc"}'
```

The ReAct Agent is bounded for demo safety: maximum 3 reasoning loops and 40 seconds total runtime.

The API uses local documents from `src/vinwonders_knowledge.py`, retrieves the most relevant context,
then asks the configured self-hosted model through Ollama.

### 4. Run the CLI Chatbot Baseline
Interactive mode:
```bash
python3 -m src.chatbot
```

One-shot mode:
```bash
python3 -m src.chatbot --message "Gợi ý trò chơi nước ở Phú Quốc"
```

### 5. Directory Structure
- `src/tools/`: Extension point for your custom tools.

## 🏠 Running with Local Models (CPU)

If you don't want to use OpenAI or Gemini, you can run open-source models (like Phi-3) directly on your CPU using `llama-cpp-python`.

### 1. Download the Model
Download the **Phi-3-mini-4k-instruct-q4.gguf** (approx 2.2GB) from Hugging Face:
- [Phi-3-mini-4k-instruct-GGUF](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf)
- Direct Download: [phi-3-mini-4k-instruct-q4.gguf](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf)

### 2. Place Model in Project
Create a `models/` folder in the root and move the downloaded `.gguf` file there.

### 3. Update `.env`
Change your `DEFAULT_PROVIDER` and set the path:
```env
DEFAULT_PROVIDER=local
LOCAL_MODEL_PATH=./models/Phi-3-mini-4k-instruct-q4.gguf
```

## 🎯 Lab Objectives

1.  **Baseline Chatbot**: Observe the limitations of a standard LLM when faced with multi-step reasoning.
2.  **ReAct Loop**: Implement the `Thought-Action-Observation` cycle in `src/agent/agent.py`.
3.  **Provider Switching**: Swap between OpenAI and Gemini seamlessly using the `LLMProvider` interface.
4.  **Failure Analysis**: Use the structured logs in `logs/` to identify why the agent fails (hallucinations, parsing errors).
5.  **Grading & Bonus**: Follow the [SCORING.md](file:///Users/tindt/personal/ai-thuc-chien/day03-lab-agent/SCORING.md) to maximize your points and explore bonus metrics.

## 🛠️ How to Use This Baseline
The code is designed as a **Production Prototype**. It includes:
- **Telemetry**: Every action is logged in JSON format for later analysis.
- **Robust Provider Pattern**: Easily extendable to any LLM API.
- **Clean Skeletons**: Focus on the logic that matters—the agent's reasoning process.

---

*Happy Coding! Let's build agents that actually work.*
