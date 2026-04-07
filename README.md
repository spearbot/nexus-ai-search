# ⬡ Nexus · Intelligent Research Cortex

> An AI-powered **multi-query research engine** that performs deep web retrieval and generates structured intelligence briefs — powered by **LangChain**, **Ollama (local LLMs)**, **FAISS**, and **Streamlit**.

Nexus doesn’t just search — it **thinks like a research analyst**.

It decomposes your query into multiple semantic angles, retrieves information across the web, and synthesizes a structured report with insights, trends, and research gaps.

---

# 🧠 Pipeline Architecture

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
④ Vector Embedding (Local - HuggingFace)
    Chunks text → embeds → builds FAISS index
    │
    ▼
⑤ Multi-Query Retrieval + Dedup
    Retrieves top-k chunks across queries, merges unique results
    │
    ▼
⑥ LLM Synthesis (Ollama - Llama3)
    Generates structured intelligence brief
    │
    ▼
Intelligence Brief
  · Overview · Key Findings · Emerging Signals
  · Research Gaps · Confidence / Coverage / Gap scores
```

---

# 🚀 Quick Start

## 1. Install Ollama

👉 [https://ollama.com](https://ollama.com)

---

## 2. Pull a model

```bash
ollama pull llama3
```

---

## 3. Run the project

### Mac / Linux

```bash
unzip nexus.zip && cd nexus
bash run.sh
```

### Windows

Double-click:

```bash
run.bat
```

---

## 4. Start Ollama (important)

```bash
ollama run llama3
```

---

## 5. Open app

```
http://localhost:8501
```

---

# 🔑 Environment Variables

Only **Google Search API** is required now:

```env
GOOGLE_API_KEY=your_key
GOOGLE_CSE_ID=your_id
```

👉 No LLM API keys needed (runs locally)

---

# ⚡ What Makes Nexus Different

| Feature        | Basic RAG    | Nexus                         |
| -------------- | ------------ | ----------------------------- |
| Query strategy | Single query | Multi-query decomposition     |
| Retrieval      | Sequential   | Parallel search               |
| Deduplication  | None         | URL + semantic dedup          |
| LLM            | API-based    | Local (Ollama)                |
| Output         | Plain text   | Structured intelligence brief |
| Insights       | None         | Trends + gaps + scoring       |

---

# 🏗️ Project Structure

```
nexus/
├── app.py            # Streamlit UI + pipeline visualisation
├── nexus_engine.py   # Core multi-query RAG engine
├── requirements.txt
├── .env.example
├── run.sh
├── run.bat
└── README.md
```

---

# 🛠️ Tech Stack

| Layer         | Tool                      |
| ------------- | ------------------------- |
| UI            | Streamlit                 |
| LLM           | Ollama (Llama3 / Mistral) |
| Embeddings    | HuggingFace (local)       |
| Vector DB     | FAISS                     |
| Orchestration | LangChain                 |
| Search        | Google Custom Search API  |
| Scraping      | BeautifulSoup             |
| Concurrency   | concurrent.futures        |

---

# 🧠 Key Features

* 🔍 Multi-query search for broader coverage
* ⚡ Parallel web retrieval
* 🧹 Smart content cleaning & chunking
* 🧠 Local LLM reasoning (no API limits)
* 📊 Structured research output
* 🧪 Research gap detection
* 🎯 Confidence & coverage scoring

---

# ⚠️ Limitations

* Web scraping may fail on some sites (anti-bot protection)
* Local models are slower than cloud APIs
* Quality depends on retrieved content

---

# 🚀 Future Improvements

* Better ranking / reranking (BM25 / hybrid search)
* Streaming responses (ChatGPT-style)
* PDF & file upload support
* Caching layer (Redis)
* Deployment (Docker + cloud)

---

# 🧠 Inspiration

Inspired by systems like:

* Perplexity AI
* OpenAI research workflows

---

# 👨‍💻 Author

Built by **Kartik**
AI/ML student building real-world systems 🚀

