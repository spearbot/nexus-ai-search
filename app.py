import html
import streamlit as st
import os
from dotenv import load_dotenv
from ohara_engine import OharaEngine

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ohara · Research Cortex",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:       #080b10;
    --surface:  #0e1218;
    --surface2: #141920;
    --border:   #1f2733;
    --border2:  #2a3545;
    --accent:   #00e5ff;
    --accent2:  #7b61ff;
    --green:    #00ff9d;
    --amber:    #ffb020;
    --red:      #ff4d6d;
    --text:     #d8e3f0;
    --muted:    #5a6a80;
    --dim:      #3a4a60;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 1.5rem 4rem; max-width: 820px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

/* ── Masthead ── */
.nx-masthead {
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.nx-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}
.nx-hex {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    clip-path: polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
    flex-shrink: 0;
}
.nx-wordmark {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #fff;
    line-height: 1;
}
.nx-wordmark span { color: var(--accent); }
.nx-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-left: 3.3rem;
}

/* ── Input ── */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 8px !important;
    padding: 0.85rem 1.1rem !important;
    font-size: 1rem !important;
    font-family: 'Syne', sans-serif !important;
    color: #fff !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,229,255,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }
.stTextInput label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Selectors ── */
.stSelectbox > div > div,
.stSlider > div {
    background: var(--surface) !important;
}
.stSelectbox label, .stSlider label, .stNumberInput label {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stSelectbox > div > div > div {
    color: var(--text) !important;
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.15s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

/* ── Pipeline box ── */
.pipeline-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin: 1.5rem 0;
    font-family: 'JetBrains Mono', monospace;
}
.pipeline-box .pb-title {
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.pipeline-step {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    margin-bottom: 0.6rem;
    font-size: 0.8rem;
    color: var(--dim);
}
.pipeline-step.done  { color: var(--green); }
.pipeline-step.active { color: var(--accent); }
.pipeline-step.error  { color: var(--red); }
.ps-icon { flex-shrink: 0; width: 1rem; text-align: center; }
.ps-label { flex: 1; }
.ps-detail {
    font-size: 0.7rem;
    color: var(--muted);
    margin-top: 0.15rem;
}

/* ── Query variants ── */
.qv-row {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
    margin: 0.5rem 0 1rem;
}
.qv-item {
    background: var(--surface2);
    border-left: 3px solid var(--accent2);
    border-radius: 0 6px 6px 0;
    padding: 0.5rem 0.9rem;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text);
}
.qv-item:nth-child(2) { border-color: var(--accent); }
.qv-item:nth-child(3) { border-color: var(--green); }
.qv-num {
    color: var(--muted);
    margin-right: 0.5rem;
    font-size: 0.7rem;
}

/* ── Result card ── */
.nx-card {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 2rem 2.2rem;
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
}
.nx-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--green));
}
.nx-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
    gap: 1rem;
}
.nx-card-topic {
    font-size: 1.35rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: -0.3px;
    line-height: 1.3;
}
.nx-badge {
    background: rgba(0,229,255,0.1);
    border: 1px solid rgba(0,229,255,0.25);
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    padding: 0.25rem 0.65rem;
    border-radius: 20px;
    white-space: nowrap;
    letter-spacing: 0.08em;
    flex-shrink: 0;
}
.nx-badge.green {
    background: rgba(0,255,157,0.08);
    border-color: rgba(0,255,157,0.2);
    color: var(--green);
}
.nx-badge.amber {
    background: rgba(255,176,32,0.08);
    border-color: rgba(255,176,32,0.2);
    color: var(--amber);
}

/* ── Section headings ── */
.nx-sec {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    color: var(--muted);
    text-transform: uppercase;
    padding: 1.5rem 0 0.6rem;
    border-top: 1px solid var(--border);
    margin-top: 1.2rem;
}
.nx-sec:first-of-type { border-top: none; margin-top: 0; padding-top: 0; }

/* ── Body text ── */
.nx-body {
    font-size: 0.93rem;
    line-height: 1.8;
    color: var(--text);
}
.nx-body ul { padding-left: 1.2rem; margin: 0.4rem 0; }
.nx-body li { margin-bottom: 0.4rem; }

/* ── Confidence bar ── */
.conf-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 0.5rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
}
.conf-label { color: var(--muted); width: 5rem; flex-shrink: 0; }
.conf-track {
    flex: 1;
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    overflow: hidden;
}
.conf-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
}
.conf-val { color: var(--text); width: 2.5rem; text-align: right; }

/* ── Source chips ── */
.src-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.7rem;
}
.src-chip {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.35rem 0.8rem;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--muted);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    transition: border-color 0.15s, color 0.15s;
}
.src-chip:hover { border-color: var(--accent); color: var(--accent); }
.src-num {
    background: var(--border);
    color: var(--accent);
    border-radius: 3px;
    padding: 0 0.3rem;
    font-size: 0.65rem;
}

/* ── History separator ── */
.hist-sep {
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--dim);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 2rem 0 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.hist-sep::before, .hist-sep::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 0;
}
.empty-hex {
    width: 56px; height: 56px;
    background: var(--surface);
    border: 1px solid var(--border);
    clip-path: polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
    margin: 0 auto 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}
.empty-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.1em;
}
.empty-hint {
    font-size: 0.82rem;
    color: var(--dim);
    margin-top: 0.4rem;
}

/* ── Number input ── */
.stNumberInput > div > div > input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Chunk counter ── */
.chunk-counter {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 0.3rem;
}
.chunk-counter span { color: var(--accent); font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nx-masthead">
    <div class="nx-logo">
        <div class="nx-hex"></div>
        <div class="nx-wordmark">NEX<span>US</span></div>
    </div>
    <div class="nx-sub">Intelligent Research Cortex · Multi-Query RAG Pipeline</div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Input area ────────────────────────────────────────────────────────────────
query = st.text_input(
    "Research Query",
    placeholder="e.g.  Neuromorphic computing in edge AI systems",
)

col1, col2 = st.columns([2, 1])
with col1:
    focus = st.selectbox(
        "Focus Mode",
        ["Comprehensive Overview", "Technical Deep-Dive", "Current Developments", "Comparative Analysis"],
    )
with col2:
    num_sources = st.number_input("Sources", min_value=3, max_value=8, value=5)

run = st.button("⬡  Initialise Research Pipeline")


# ── Engine factory ────────────────────────────────────────────────────────────
def get_engine():
    gak = os.getenv("GOOGLE_API_KEY")
    cse = os.getenv("GOOGLE_CSE_ID")
    model = os.getenv("OLLAMA_MODEL", "llama3")
    if not all([gak, cse]):
        st.error("⚠️  Set GOOGLE_API_KEY and GOOGLE_CSE_ID in your .env file.")
        st.stop()
    return OharaEngine(google_api_key=gak, google_cse_id=cse, model=model)


# ── Pipeline UI runner ────────────────────────────────────────────────────────
STEPS = [
    ("decompose",  "Query Decomposition",     "Generating 3 semantic query variants"),
    ("search",     "Parallel Web Retrieval",  "Fetching sources across all query axes"),
    ("scrape",     "Content Extraction",      "Parsing & cleaning raw page content"),
    ("embed",      "Vector Embedding",        "Chunking + embedding via HuggingFace"),
    ("retrieve",   "Semantic Retrieval",      "Scoring & deduplicating top-k chunks"),
    ("synthesise", "LLM Synthesis",           "Generating structured intelligence brief"),
]

def render_pipeline(done_keys: list[str], active_key: str | None = None, error_key: str | None = None):
    rows = ""
    for key, label, detail in STEPS:
        if key == error_key:
            cls, icon = "error", "✗"
        elif key in done_keys:
            cls, icon = "done", "✓"
        elif key == active_key:
            cls, icon = "active", "▶"
        else:
            cls, icon = "", "○"
        escaped_label = html.escape(label)
        escaped_detail = html.escape(detail)
        rows += f"""
        <div class="pipeline-step {cls}">
            <span class="ps-icon">{icon}</span>
            <div class="ps-label">
                {escaped_label}
                <div class="ps-detail">{escaped_detail}</div>
            </div>
        </div>"""
    return f"""
    <div class="pipeline-box">
        <div class="pb-title">⬡ &nbsp;Pipeline Status</div>
        {rows}
    </div>"""


def run_step(step_key: str, step_label: str, func, pipeline_slot, done, *args, **kwargs):
    pipeline_slot.markdown(render_pipeline(done, step_key), unsafe_allow_html=True)
    try:
        result = func(*args, **kwargs)
        done.append(step_key)
        return result
    except Exception as e:
        pipeline_slot.markdown(render_pipeline(done, error_key=step_key), unsafe_allow_html=True)
        st.error(f"**{step_label}** failed: {e}")
        st.stop()


if run and query.strip():
    engine = get_engine()

    if not engine.check_ollama():
        st.error("⚠️  Ollama is not running. Start it with `ollama run llama3` (or your model) and try again.")
        st.stop()

    pipeline_slot = st.empty()
    queries_slot  = st.empty()
    done: list[str] = []

    escaped_query = html.escape(query.strip())

    # Step 1 — decompose
    variants = run_step("decompose", "Query Decomposition", engine.decompose_query, pipeline_slot, done, query.strip(), focus)

    qv_html = "".join(
        f'<div class="qv-item"><span class="qv-num">Q{i+1}</span>{html.escape(v)}</div>'
        for i, v in enumerate(variants)
    )
    queries_slot.markdown(
        f'<div class="qv-row">{qv_html}</div>',
        unsafe_allow_html=True,
    )

    # Step 2 — search
    all_sources = run_step("search", "Parallel Web Retrieval", engine.parallel_search, pipeline_slot, done, variants, num_sources)

    # Step 3 — scrape
    scraped = run_step("scrape", "Content Extraction", engine.scrape_sources, pipeline_slot, done, all_sources)

    # Step 4 — embed + vectorstore
    store, chunk_count = run_step("embed", "Vector Embedding", engine.build_store, pipeline_slot, done, scraped)

    # Step 5 — retrieve
    chunks = run_step("retrieve", "Semantic Retrieval", engine.retrieve, pipeline_slot, done, store, variants)

    # Step 6 — synthesise
    result = run_step("synthesise", "LLM Synthesis", engine.synthesise, pipeline_slot, done, query.strip(), focus, chunks, all_sources)

    pipeline_slot.markdown(render_pipeline(done), unsafe_allow_html=True)

    result["query"]       = escaped_query
    result["variants"]    = variants
    result["sources"]     = all_sources
    result["chunk_count"] = chunk_count
    st.session_state.history.insert(0, result)

elif run and not query.strip():
    st.warning("Enter a research query to initialise the pipeline.")


# ── Render results ────────────────────────────────────────────────────────────
for idx, r in enumerate(st.session_state.history):
    conf = r.get("confidence", 72)
    cov  = r.get("coverage",   68)
    gap  = r.get("gap_score",  55)

    conf_color = "green" if conf >= 75 else "amber" if conf >= 55 else "red"

    src_chips = "".join(
        f'<a class="src-chip" href="{html.escape(s["url"])}" target="_blank">'
        f'<span class="src-num">{i+1}</span>{html.escape(s["title"][:36])}{"…" if len(s["title"])>36 else ""}'
        f'</a>'
        for i, s in enumerate(r.get("sources", []))
    )

    overview = r.get("overview", "")
    key_findings = r.get("key_findings", "")
    emerging_trends = r.get("emerging_trends", "")
    research_gaps = r.get("research_gaps", "")
    query_display = r.get("query", "")
    chunk_count = r.get("chunk_count", 0)
    sources_list = r.get("sources", [])

    st.markdown(f"""
    <div class="nx-card">
        <div class="nx-card-header">
            <div class="nx-card-topic">{query_display}</div>
            <div class="nx-badge {conf_color}">CONF {conf}%</div>
        </div>

        <div class="nx-sec">Intelligence Overview</div>
        <div class="nx-body">{overview}</div>

        <div class="nx-sec">Key Intelligence Points</div>
        <div class="nx-body">{key_findings}</div>

        <div class="nx-sec">Emerging Signals</div>
        <div class="nx-body">{emerging_trends}</div>

        <div class="nx-sec">Research Gaps Detected</div>
        <div class="nx-body">{research_gaps}</div>

        <div class="nx-sec">Signal Quality</div>
        <div class="conf-row">
            <span class="conf-label">Confidence</span>
            <div class="conf-track"><div class="conf-fill" style="width:{conf}%"></div></div>
            <span class="conf-val">{conf}%</span>
        </div>
        <div class="conf-row">
            <span class="conf-label">Coverage</span>
            <div class="conf-track"><div class="conf-fill" style="width:{cov}%"></div></div>
            <span class="conf-val">{cov}%</span>
        </div>
        <div class="conf-row">
            <span class="conf-label">Gap Index</span>
            <div class="conf-track"><div class="conf-fill" style="width:{gap}%; background: linear-gradient(90deg,#ff4d6d,#ffb020)"></div></div>
            <span class="conf-val">{gap}%</span>
        </div>

        <div class="nx-sec">Sources · {len(sources_list)} indexed · <span style="color:var(--accent)">{chunk_count}</span> chunks embedded</div>
        <div class="src-grid">{src_chips}</div>
    </div>
    """, unsafe_allow_html=True)

    if idx < len(st.session_state.history) - 1:
        st.markdown('<div class="hist-sep">Previous Query</div>', unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.history:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-hex">⬡</div>
        <div class="empty-label">Ohara is standing by</div>
        <div class="empty-hint">Enter a query above to initialise the research pipeline</div>
    </div>
    """, unsafe_allow_html=True)
