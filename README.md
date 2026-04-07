# ⬡ Nexus · Intelligent Research Cortex

> A multi-query RAG research pipeline built with **LangChain**, **Google Gemini**, **FAISS**, and **Streamlit**.

Nexus doesn't just search — it decomposes your query into 3 semantic variants, retrieves content in parallel, deduplicates across all result sets, and synthesises a structured intelligence brief with confidence scoring and research gap detection.

---

## Pipeline Architecture

```
User Query
    │
    ▼
① Query Decomposition (Gemini)
    Rewrites query into 3 semantic variants for max retrieval coverage
    │
    ▼
② Parallel Web Retrieval (Google Custom Search × 3)
    Runs all variants simultaneously, deduplicates URLs
    │
    ▼
③ Content Extraction (BeautifulSoup)
    Scrapes full page text concurrently (6 workers)
    │
    ▼
④ Vector Embedding (Google Generative AI Embeddings)
    Chunks text → embeds → builds FAISS in-memory index
    │
    ▼
⑤ Multi-Query Retrieval + Dedup
    Retrieves top-k chunks per variant, merges unique results
    │
    ▼
⑥ LLM Synthesis (Gemini 1.5 Flash)
    Generates structured JSON brief with scores
    │
    ▼
Intelligence Brief
  · Overview · Key Findings · Emerging Signals
  · Research Gaps · Confidence / Coverage / Gap scores
```

---

## Quick Start

### Mac / Linux
```bash
unzip nexus.zip && cd nexus
bash run.sh
```

### Windows
Double-click `run.bat`

The script will:
1. Check Python is installed
2. Create `.env` from template on first run (auto-opens for editing)
3. Install all dependencies
4. Launch the Streamlit app at http://localhost:8501

---

## API Keys (all free tier)

| Key | Get it at |
|-----|-----------|
| `GOOGLE_API_KEY` | [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials |
| `GOOGLE_CSE_ID` | [Programmable Search Engine](https://programmablesearchengine.google.com/) → Create → Search entire web |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/app/apikey) |

---

## What Makes It Different

| Feature | Basic RAG | Nexus |
|---------|-----------|-------|
| Query strategy | Single query | 3 semantic variants |
| Retrieval | Sequential | Parallel (concurrent.futures) |
| Deduplication | None | URL-level + chunk-level |
| Output | Summary | Structured JSON brief |
| Scoring | None | Confidence / Coverage / Gap Index |
| Gap detection | None | LLM-identified research gaps |

---

## Project Structure

```
nexus/
├── app.py            # Streamlit UI with live pipeline tracker
├── nexus_engine.py   # Multi-query RAG pipeline
├── requirements.txt
├── .env.example
├── run.sh            # Mac/Linux launcher
├── run.bat           # Windows launcher
└── README.md
```

---

## Tech Stack

| Layer | Tool |
|-------|------|
| UI | Streamlit |
| LLM + Embeddings | Google Gemini 1.5 Flash + embedding-001 |
| Vector Store | FAISS (in-memory) |
| Orchestration | LangChain |
| Web Search | Google Custom Search API |
| Parallelism | concurrent.futures |
| Scraping | BeautifulSoup4 |
