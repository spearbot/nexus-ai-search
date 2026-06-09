"""
ohara_engine.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Multi-Query RAG Pipeline:

  1. decompose_query()  → Ollama rewrites query into 3 semantic variants
  2. parallel_search()  → Google CSE for each variant, deduplicated
  3. scrape_sources()   → BeautifulSoup full-page extraction
  4. build_store()      → Chunk + embed → FAISS vector store
  5. retrieve()         → Multi-query retrieval + deduplication
  6. synthesise()       → Ollama structured intelligence brief
"""

from __future__ import annotations

import json
import re
import requests
import concurrent.futures
import threading
from typing import Any

from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from bs4 import BeautifulSoup


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _scrape(url: str, timeout: int = 8) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Ohara-Research/1.0)"}
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)
        return text[:10_000]
    except Exception:
        return ""


def _clean_json(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    return raw.strip()


def _make_document(text: str, source: str, title: str) -> Document:
    return Document(
        page_content=text,
        metadata={"source": source, "title": title},
    )


# ─────────────────────────────────────────────────────────────────────────────
# Prompts
# ─────────────────────────────────────────────────────────────────────────────

DECOMPOSE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expert research strategist. Your job is to decompose a user's "
     "research query into 3 semantically distinct variants that together maximise "
     "retrieval coverage. Each variant should approach the topic from a different angle.\n"
     "Return ONLY a JSON array of 3 strings. No markdown, no explanation."),
    ("human",
     "Query: {query}\nFocus mode: {focus}\n\n"
     "Return exactly: [\"variant1\", \"variant2\", \"variant3\"]"),
])

SYNTHESIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are Ohara, an elite research intelligence system. "
     "Synthesise the provided source excerpts into a structured intelligence brief. "
     "Be precise, analytical, and cite evidence from the context. "
     "Return ONLY valid JSON — no markdown fences, no extra keys."),
    ("human",
     """Original Query: {query}
Focus Mode: {focus}

Source Excerpts:
{context}

Return a JSON object with EXACTLY these keys:
{{
  "overview": "<3-4 sentence analytical overview in plain text>",
  "key_findings": "<HTML unordered list (<ul><li>…</li></ul>) of 5-7 precise findings>",
  "emerging_trends": "<HTML unordered list (<ul><li>…</li></ul>) of 3-4 emerging signals or developments>",
  "research_gaps": "<HTML unordered list (<ul><li>…</li></ul>) of 2-3 gaps or unanswered questions detected>",
  "confidence": <integer 40-95 reflecting how well sources cover the topic>,
  "coverage": <integer 40-95 reflecting breadth of source perspectives>,
  "gap_score": <integer 20-80 reflecting how many open questions remain>
}}"""),
])


# ─────────────────────────────────────────────────────────────────────────────
# Engine
# ─────────────────────────────────────────────────────────────────────────────

class OharaEngine:

    def __init__(
        self,
        google_api_key: str,
        google_cse_id: str,
        model: str = "llama3",
    ):
        self.google_api_key = google_api_key
        self.cse_id = google_cse_id
        self.model = model
        self._url_lock = threading.Lock()

        self.llm = ChatOllama(
            model=model,
            temperature=0.25,
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    # ── Health Check ────────────────────────────────────────────────────────

    def check_ollama(self) -> bool:
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    # ── 1. Query Decomposition ────────────────────────────────────────────────

    def decompose_query(self, query: str, focus: str) -> list[str]:
        chain = DECOMPOSE_PROMPT | self.llm | StrOutputParser()
        raw = chain.invoke({"query": query, "focus": focus})
        try:
            variants = json.loads(_clean_json(raw))
            if isinstance(variants, list) and len(variants) >= 3:
                return variants[:3]
        except Exception:
            pass
        return [
            query,
            f"{query} — recent developments and research",
            f"{query} — technical analysis and applications",
        ]

    # ── 2. Parallel Web Search ────────────────────────────────────────────────

    def _search_one(self, query: str, num: int) -> list[dict]:
        try:
            r = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params={"key": self.google_api_key, "cx": self.cse_id, "q": query, "num": min(num, 10)},
                timeout=10,
            )
            r.raise_for_status()
            return [
                {"title": i.get("title", ""), "url": i.get("link", ""), "snippet": i.get("snippet", "")}
                for i in r.json().get("items", [])
            ]
        except Exception:
            return []

    def parallel_search(self, variants: list[str], num_per_query: int = 4) -> list[dict]:
        seen_urls: set[str] = set()
        all_sources: list[dict] = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
            futures = {ex.submit(self._search_one, v, num_per_query): v for v in variants}
            for fut in concurrent.futures.as_completed(futures):
                for src in fut.result():
                    with self._url_lock:
                        if src["url"] not in seen_urls:
                            seen_urls.add(src["url"])
                            all_sources.append(src)

        return all_sources[:12]

    # ── 3. Scrape Sources ─────────────────────────────────────────────────────

    def scrape_sources(self, sources: list[dict]) -> list[dict]:
        def _fetch(src: dict) -> dict:
            text = _scrape(src["url"])
            if not text or len(text) < 200:
                text = f"{src.get('title','')} {src.get('snippet','')}"
            return {**src, "text": text}

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
            return list(ex.map(_fetch, sources))

    # ── 4. Build Vector Store ─────────────────────────────────────────────────

    def build_store(self, scraped: list[dict]) -> tuple[FAISS, int]:
        docs: list[Document] = []
        for src in scraped:
            if not src.get("text"):
                continue
            chunks = self.splitter.create_documents(
                [src["text"]],
                metadatas=[{"source": src["url"], "title": src["title"]}],
            )
            docs.extend(chunks)

        if not docs:
            docs = [
                _make_document(
                    f"{s.get('title','')} {s.get('snippet','')}",
                    s.get("url", ""),
                    s.get("title", ""),
                )
                for s in scraped if s.get("snippet") or s.get("title")
            ]

        if not docs:
            docs = [
                _make_document("Fallback content for embedding", "none", "fallback"),
            ]

        store = FAISS.from_documents(docs, self.embeddings)
        return store, len(docs)

    # ── 5. Multi-Query Retrieval + Dedup ──────────────────────────────────────

    def retrieve(self, store: FAISS, variants: list[str], k: int = 6) -> list[Document]:
        retriever = store.as_retriever(search_kwargs={"k": k})
        seen: set[str] = set()
        merged: list[Document] = []

        for q in variants:
            for doc in retriever.invoke(q):
                key = doc.page_content[:120]
                if key not in seen:
                    seen.add(key)
                    merged.append(doc)

        return merged[:20]

    # ── 6. Synthesise Brief ───────────────────────────────────────────────────

    def synthesise(
        self,
        query: str,
        focus: str,
        chunks: list[Document],
        sources: list[dict],
    ) -> dict[str, Any]:
        if not chunks:
            return {
                "overview": "No retrievable content was found for this query. "
                            "The web search did not return any usable sources.",
                "key_findings": "<ul><li>No sources could be retrieved or scraped.</li></ul>",
                "emerging_trends": "<ul><li>—</li></ul>",
                "research_gaps": "<ul><li>—</li></ul>",
                "confidence": 0,
                "coverage": 0,
                "gap_score": 100,
            }

        context = "\n\n---\n\n".join(
            f"[Source: {d.metadata.get('title','?')}]\n{d.page_content}"
            for d in chunks
        )

        chain = SYNTHESIS_PROMPT | self.llm | StrOutputParser()
        raw = chain.invoke({"query": query, "focus": focus, "context": context})

        try:
            result = json.loads(_clean_json(raw))
        except Exception:
            result = {
                "overview": raw,
                "key_findings": "<ul><li>Could not parse structured output.</li></ul>",
                "emerging_trends": "<ul><li>—</li></ul>",
                "research_gaps": "<ul><li>—</li></ul>",
                "confidence": 50,
                "coverage": 50,
                "gap_score": 50,
            }

        return result
