#!/bin/bash
# ── Ohara Research Cortex · Quick Start ──────────────────────────────────────

echo ""
echo "  ⬡  OHARA Research Cortex"
echo "  ─────────────────────────"

if ! command -v python3 &>/dev/null; then
    echo "  ❌  Python 3 not found. Install from https://python.org"
    exit 1
fi

if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "  ⚠️   Created .env from template."
    echo "  👉  Open .env, add your 3 API keys, then re-run."
    echo ""
    command -v open &>/dev/null && open .env
    exit 0
fi

echo "  📦  Installing dependencies..."
pip install -r requirements.txt -q

echo "  🚀  Launching Ohara..."
echo ""
streamlit run app.py
