# ⬡ Ohara · Research Engine

> AI-powered **multi-query research engine** that performs deep web retrieval and generates structured intelligence briefs — powered by **LangChain**, **Ollama (local LLMs)**, **FAISS**, and **Streamlit**.

Ohara decomposes your query into multiple semantic search angles, retrieves information from across the web, and synthesizes a structured report with findings, trends, and research gaps.

---

## Pipeline Architecture

```
User Query
    │
    ▼
① Query Decomposition (Ollama)
    Generates 3 semantic variants for broader coverage
    │
    ▼
② Parallel Web Retrieval (Google CSE × 3)
    Executes all variants concurrently, deduplicates sources
    │
    ▼
③ Content Extraction (BeautifulSoup)
    Scrapes and cleans page content (multi-threaded)
    │
    ▼
④ Vector Embedding (Local — HuggingFace)
    Chunks text → embeds → builds FAISS index
    │
    ▼
⑤ Multi-Query Retrieval + Dedup
    Retrieves top-k chunks across queries, merges unique results
    │
    ▼
⑥ LLM Synthesis (Ollama)
    Generates structured intelligence brief
    │
    ▼
Intelligence Brief
  · Overview · Key Findings · Emerging Signals
  · Research Gaps · Confidence / Coverage / Gap scores
```

---

## Quick Start

### 1. Install Ollama

<https://ollama.com>

### 2. Pull a model

```bash
ollama pull llama3
```

### 3. Set up environment

```bash
cd nexus-ai-search
cp .env.example .env
# Edit .env with your Google API key and CSE ID
```

### 4. Start Ollama

```bash
ollama run llama3
```

### 5. Run the app

```bash
bash run.sh
```

Then open **http://localhost:8501**

---

## Environment Variables

| Variable         | Required | Default    | Description                        |
|------------------|----------|------------|------------------------------------|
| `GOOGLE_API_KEY` | Yes      | —          | Google Custom Search API key       |
| `GOOGLE_CSE_ID`  | Yes      | —          | Google Custom Search Engine ID     |
| `OLLAMA_MODEL`   | No       | `llama3`   | Ollama model name                  |

No LLM API keys needed — everything runs locally via Ollama.

---

## What Makes Ohara Different

| Feature        | Basic RAG    | Ohara                          |
|----------------|--------------|--------------------------------|
| Query strategy | Single query | Multi-query decomposition      |
| Retrieval      | Sequential   | Parallel search                |
| Deduplication  | None         | URL + content dedup            |
| LLM            | API-based    | Local (Ollama)                 |
| Output         | Plain text   | Structured intelligence brief  |
| Error handling | Crash on fail | Per-step recovery + UI alerts  |

---

## Project Structure

```
ohara/
├── app.py             # Streamlit UI + pipeline visualisation
├── ohara_engine.py    # Core multi-query RAG engine
├── requirements.txt
├── .env.example
├── run.sh
├── run.bat
└── README.md
```

---

## Tech Stack

| Layer         | Tool                      |
|---------------|---------------------------|
| UI            | Streamlit                 |
| LLM           | Ollama (Llama3 / Mistral) |
| Embeddings    | HuggingFace (local)       |
| Vector DB     | FAISS                     |
| Orchestration | LangChain                 |
| Search        | Google Custom Search API  |
| Scraping      | BeautifulSoup             |
| Concurrency   | concurrent.futures        |

---

## Key Features

- **Multi-query search** — decomposes queries into 3 semantic variants for broader coverage
- **Parallel retrieval** — fetches sources concurrently across all query axes
- **Smart content cleaning** — strips boilerplate, chunks intelligently
- **Local LLM reasoning** — no API limits or costs (Ollama)
- **Per-step error handling** — pipeline shows which step failed with a clear message
- **Ollama health check** — verifies Ollama is running before starting the pipeline
- **Configurable model** — set `OLLAMA_MODEL` in `.env` (defaults to `llama3`)
- **Structured output** — overview, findings, trends, research gaps, and quality scores
- **Session history** — previous results remain visible during the session

---

## Limitations

- Web scraping may fail on some sites (anti-bot protection)
- Local models are slower than cloud APIs
- Quality depends on retrieved content
- History is ephemeral (lost on page refresh)

---

## Future Improvements

- Better ranking / reranking (BM25 / hybrid search)
- Streaming responses (ChatGPT-style)
- PDF & file upload support
- Caching layer (Redis)
- Deployment (Docker + cloud)

---

## Author

Built by **Kartik** — AI/ML student building real-world systems
