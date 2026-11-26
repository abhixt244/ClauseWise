"""Reusable UI rendering helpers and data utilities for ClauseWise."""

import html
import re
from typing import Any, Dict, List

import streamlit as st

from ui.icons import lucide_icon

# Matches backend/risk.py indicators purely for deterministic highlighting of extracted source text.
_HIGH_RISK_TERMS = [
    "indemnify",
    "indemnification",
    "hold harmless",
    "unlimited liability",
    "sole discretion",
    "unilateral",
    "irrevocable",
    "perpetual",
    "exclusive rights",
    "waive",
    "waiver",
    "non-compete",
    "non-solicitation",
]

_MEDIUM_RISK_TERMS = [
    "termination",
    "breach",
    "default",
    "remedy",
    "arbitration",
    "jurisdiction",
    "governing law",
    "confidential",
    "proprietary",
    "intellectual property",
]


def render_html(markup: str) -> None:
    """Render HTML cleanly without CommonMark blank-line or 4-space indentation pitfalls."""
    lines = [line.strip() for line in markup.splitlines() if line.strip()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def clean_text(text: Any) -> str:
    """Strip any stray HTML tags and normalize whitespace."""
    raw = str(text) if text is not None else ""
    stripped = re.sub(r"<[^>]+>", "", raw)
    return re.sub(r"\s+", " ", html.unescape(stripped)).strip()


def escape_text(text: Any) -> str:
    """Clean and HTML-escape untrusted text for safe rendering."""
    return html.escape(clean_text(text))


def detect_risk_keywords(text: str) -> List[str]:
    """Identify risk-relevant terms actually present in the extracted document passage."""
    lower = text.lower()
    found: List[str] = []
    for term in _HIGH_RISK_TERMS + _MEDIUM_RISK_TERMS:
        if term in lower:
            found.append(term)
    return found


def highlight_passage_terms(text: str, terms: List[str]) -> str:
    """Escape extracted passage text and highlight exact matched terms without altering content."""
    safe = escape_text(text)
    if not terms:
        return safe
    sorted_terms = sorted(set(terms), key=len, reverse=True)
    pattern = re.compile(r"(" + "|".join(re.escape(t) for t in sorted_terms) + r")", re.IGNORECASE)
    return pattern.sub(r'<span class="cw-kw-mark">\1</span>', safe)


def risk_badge(risk: str) -> str:
    """Return consistent pill badge HTML for HIGH, MEDIUM, or LOW risk."""
    level = str(risk or "MEDIUM").upper().strip()
    if level == "HIGH":
        return f'<span class="cw-pill cw-pill-high">{lucide_icon("shield-alert", 12)}High</span>'
    if level == "LOW":
        return f'<span class="cw-pill cw-pill-low">{lucide_icon("check-circle", 12)}Low</span>'
    return f'<span class="cw-pill cw-pill-medium">{lucide_icon("alert-triangle", 12)}Medium</span>'


def page_header(title: str, description: str, badge_html: str = "") -> None:
    """Render standardized Linear-style page header."""
    badge_block = f"<div>{badge_html}</div>" if badge_html else ""
    render_html(
        f"""
        <div class="cw-page-header">
            <div>
                <div class="cw-page-title" role="heading" aria-level="1">{html.escape(title)}</div>
                <p class="cw-page-desc">{html.escape(description)}</p>
            </div>
            {badge_block}
        </div>
        """
    )


def compute_risk_counts(clauses: List[Dict[str, Any]]) -> Dict[str, int]:
    """Count clauses by normalized risk level."""
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for clause in clauses:
        level = str(clause.get("risk", "MEDIUM")).upper().strip()
        if level in counts:
            counts[level] += 1
    return counts


def format_file_size(num_bytes: int) -> str:
    """Human-readable byte formatter."""
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 * 1024):.2f} MB"
