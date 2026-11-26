"""Document Review & Clause Citation Workspace for ClauseWise."""

from datetime import datetime
import html
import json
from typing import Any, Dict, List, Tuple

import streamlit as st

from services.state import get_active_record
from ui.components import (
    clean_text,
    compute_risk_counts,
    detect_risk_keywords,
    highlight_passage_terms,
    page_header,
    render_html,
    risk_badge,
)
from ui.icons import lucide_icon

_SEVERITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}


def _build_markdown_report(filename: str, clauses: List[Dict[str, Any]], counts: Dict[str, int]) -> str:
    """Create a clean Markdown export from the real backend analysis payload."""
    lines = [
        "# ClauseWise Analysis Report\n",
        f"**Document:** {filename}",
        f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Total Clauses:** {len(clauses)}",
        f"**Risk Distribution:** High: {counts['HIGH']} | Medium: {counts['MEDIUM']} | Low: {counts['LOW']}\n",
        "---\n",
    ]
    for idx, clause in enumerate(clauses, 1):
        lines.append(f"## Clause {idx} — {str(clause.get('risk', 'MEDIUM')).upper()} Risk\n")
        lines.append(f"**Simplified:** {clean_text(clause.get('simplified', 'N/A'))}\n")
        lines.append(f"**Risk Rationale:** {clean_text(clause.get('reason', 'N/A'))}\n")
        lines.append(f"**Original Text:**\n\n> {clean_text(clause.get('original', 'N/A'))}\n")
        lines.append("---\n")
    return "\n".join(lines)


def render_workspace() -> None:
    """Render the central Document Analysis & Source Citation Workspace."""
    data = st.session_state.get("processed_data")
    filename = st.session_state.get("uploaded_file_name")

    if not data or not filename:
        page_header(
            "Review Workspace",
            "Inspect AI-generated clause summaries alongside verbatim document passages.",
        )
        render_html(
            f"""
            <div class="cw-card" style="padding:28px;max-width:680px;">
                <div style="display:flex;align-items:center;gap:10px;color:#F3F4F6;font-weight:600;font-size:1rem;margin-bottom:8px;">
                    {lucide_icon("file-text", 18, "#60A5FA")} No active document selected
                </div>
                <p style="font-size:0.87rem;color:#9CA3AF;line-height:1.55;margin:0;">
                    Upload a legal document to generate clause-level plain-English analysis and risk citations,
                    or open a previously analyzed document from Session History.
                </p>
            </div>
            """
        )
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        b1, b2, _ = st.columns([1.2, 1.2, 2.6])
        with b1:
            if st.button("Upload Document", type="primary", use_container_width=True, key="ws_empty_upload"):
                st.session_state.active_page = "New Analysis"
                st.rerun()
        with b2:
            if st.button("Session History", use_container_width=True, key="ws_empty_hist"):
                st.session_state.active_page = "History"
                st.rerun()
        return

    clauses: List[Dict[str, Any]] = data.get("clauses", [])
    counts = compute_risk_counts(clauses)
    active_rec = get_active_record()

    meta_parts = [f"{len(clauses)} clauses"]
    if active_rec:
        meta_parts.append(f"analyzed {active_rec['analyzed_at']}")
        meta_parts.append(f"{active_rec['elapsed_seconds']}s")
        meta_parts.append(active_rec["model"])

    context_badges = (
        f'<div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">'
        f'<span class="cw-pill cw-pill-high">{counts["HIGH"]} High</span>'
        f'<span class="cw-pill cw-pill-medium">{counts["MEDIUM"]} Medium</span>'
        f'<span class="cw-pill cw-pill-low">{counts["LOW"]} Low</span>'
        f"</div>"
    )
    page_header(filename, " · ".join(meta_parts), badge_html=context_badges)

    # Action & export strip
    act1, act2, act3, act4 = st.columns([2.2, 1.0, 1.0, 1.0])
    with act1:
        search_query = st.text_input(
            "Filter clauses",
            placeholder="Search clause text, plain-English summary, or rationale...",
            label_visibility="collapsed",
            key="ws_search",
        ).strip().lower()
    with act2:
        risk_filter = st.selectbox(
            "Risk level",
            ["All Risks", "HIGH", "MEDIUM", "LOW"],
            label_visibility="collapsed",
            key="ws_risk_filter",
        )
    with act3:
        sort_options = ["Document order", "Highest risk first"]
        default_idx = 0 if st.session_state.get("default_sort") == "Document order" else 1
        sort_mode = st.selectbox(
            "Sort order",
            sort_options,
            index=default_idx,
            label_visibility="collapsed",
            key="ws_sort_mode",
        )
    with act4:
        if st.button("New Analysis", use_container_width=True, key="ws_new_analysis"):
            st.session_state.active_page = "New Analysis"
            st.rerun()

    indexed_clauses: List[Tuple[int, Dict[str, Any]]] = list(enumerate(clauses, 1))
    filtered: List[Tuple[int, Dict[str, Any]]] = [
        (idx, c)
        for idx, c in indexed_clauses
        if (risk_filter == "All Risks" or str(c.get("risk", "")).upper() == risk_filter)
        and (
            not search_query
            or search_query in str(c.get("original", "")).lower()
            or search_query in str(c.get("simplified", "")).lower()
            or search_query in str(c.get("reason", "")).lower()
        )
    ]

    if sort_mode == "Highest risk first":
        filtered.sort(key=lambda pair: (_SEVERITY_ORDER.get(str(pair[1].get("risk", "MEDIUM")).upper(), 1), pair[0]))

    # Keep selected clause index valid
    valid_indices = [idx for idx, _ in filtered] or [1]
    if st.session_state.selected_clause_idx not in valid_indices and filtered:
        st.session_state.selected_clause_idx = filtered[0][0]

    st.caption(f"Displaying {len(filtered)} of {len(clauses)} extracted clauses")

    # Split workspace: Left = AI Analysis Stream, Right = Verbatim Source Citation Inspector
    left_col, right_col = st.columns([1.35, 1.0], gap="large")

    with left_col:
        render_html(
            f'<div class="cw-section-title">{lucide_icon("sparkles", 13)} AI Clause Analysis</div>'
        )
        if not filtered:
            render_html(
                """
                <div class="cw-card">
                    <div style="font-size:0.88rem;color:#9CA3AF;">
                        No clauses match your current search query or risk filter.
                    </div>
                </div>
                """
            )
        else:
            expanded_ids = set(st.session_state.get("expanded_clause_ids", set()))
            show_all_inline = bool(st.session_state.get("show_inline_source", False))

            for idx, clause in filtered:
                risk = str(clause.get("risk", "MEDIUM")).upper()
                reason_raw = clean_text(clause.get("reason", "No rationale returned."))
                keyword_flagged = "(Keyword-flagged)" in reason_raw
                reason_clean = reason_raw.replace("(Keyword-flagged)", "").strip()
                simplified_clean = clean_text(clause.get("simplified", ""))
                if not simplified_clean:
                    simplified_clean = "AI plain-English summary unavailable for this clause (fallback keyword scoring applied)."

                is_selected = st.session_state.selected_clause_idx == idx
                is_inline_open = show_all_inline or (idx in expanded_ids)
                active_cls = " cw-clause-active" if is_selected else ""
                flag_pill = (
                    f'<span class="cw-pill cw-pill-accent">{lucide_icon("shield-alert", 11)}Keyword-flagged</span>'
                    if keyword_flagged
                    else ""
                )

                inline_html = ""
                if is_inline_open:
                    orig_text = clean_text(clause.get("original", ""))
                    matched = detect_risk_keywords(orig_text)
                    highlighted_inline = highlight_passage_terms(orig_text, matched)
                    wc = len(orig_text.split()) if orig_text else 0
                    inline_html = (
                        f'<div style="margin-top:10px;padding-top:10px;border-top:1px solid #22252F;">'
                        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">'
                        f'<span class="cw-fact-tag" style="margin:0;">{lucide_icon("quote", 11)} Verbatim Source Passage</span>'
                        f'<span class="cw-pill cw-pill-neutral">{wc} words</span>'
                        f'</div>'
                        f'<div class="cw-source-passage">{highlighted_inline}</div>'
                        f'</div>'
                    )

                render_html(
                    f"""
                    <div class="cw-clause-shell{active_cls}">
                        <div class="cw-clause-meta">
                            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                                <span class="cw-clause-id">CLAUSE {idx:02d}</span>
                                {flag_pill}
                            </div>
                            {risk_badge(risk)}
                        </div>
                        <div class="cw-ai-block">
                            <div class="cw-block-tag">{lucide_icon("sparkles", 11)} AI Plain-English Summary</div>
                            <div class="cw-ai-summary">{html.escape(simplified_clean)}</div>
                        </div>
                        <div class="cw-ai-rationale">
                            <strong style="color:#E5E7EB;">Risk rationale:</strong> {html.escape(reason_clean)}
                        </div>
                        {inline_html}
                    </div>
                    """
                )
                if not show_all_inline:
                    cite_label = (
                        f"Hide Source Citation · Clause {idx:02d}"
                        if is_inline_open
                        else f"View Source Citation · Clause {idx:02d}"
                    )
                    if st.button(
                        cite_label,
                        key=f"cite_btn_{idx}",
                        type="primary" if is_inline_open else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state.selected_clause_idx = idx
                        if idx in expanded_ids:
                            expanded_ids.remove(idx)
                        else:
                            expanded_ids.add(idx)
                        st.session_state.expanded_clause_ids = expanded_ids
                        st.rerun()

    with right_col:
        render_html(
            f'<div class="cw-section-title">{lucide_icon("book-open", 13)} Extracted Document Passage</div>'
        )
        if not clauses:
            return

        sel_idx = st.session_state.selected_clause_idx
        if sel_idx < 1 or sel_idx > len(clauses):
            sel_idx = 1

        selected_clause = clauses[sel_idx - 1]
        original_raw = clean_text(selected_clause.get("original", ""))
        matched_terms = detect_risk_keywords(original_raw)
        highlighted_passage = highlight_passage_terms(original_raw, matched_terms)
        word_count = len(original_raw.split()) if original_raw else 0

        if matched_terms:
            kw_pills = "".join(
                f'<span class="cw-pill cw-pill-medium" style="margin:2px 4px 2px 0;">{html.escape(t)}</span>'
                for t in matched_terms
            )
        else:
            kw_pills = '<span style="font-size:0.79rem;color:#6B7280;">No predefined risk keywords matched in this passage.</span>'

        render_html(
            f"""
            <div class="cw-source-panel">
                <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding-bottom:10px;margin-bottom:12px;border-bottom:1px solid #22252F;">
                    <div class="cw-fact-tag" style="margin:0;">
                        {lucide_icon("quote", 12)} Verbatim Source · Clause {sel_idx:02d} of {len(clauses):02d}
                    </div>
                    <span class="cw-pill cw-pill-neutral">{word_count} words</span>
                </div>
                <div class="cw-source-passage">{highlighted_passage}</div>
                <div style="margin-top:14px;padding-top:12px;border-top:1px solid #22252F;">
                    <div class="cw-fact-tag">{lucide_icon("search", 11)} Detected Risk Terms (Factual Match)</div>
                    <div style="display:flex;flex-wrap:wrap;align-items:center;">{kw_pills}</div>
                </div>
            </div>
            """
        )

        # Previous / Next source navigation
        nav_prev, nav_next = st.columns(2)
        with nav_prev:
            if st.button(
                "Previous Clause",
                disabled=sel_idx <= 1,
                use_container_width=True,
                key="ws_prev_clause",
            ):
                st.session_state.selected_clause_idx = sel_idx - 1
                st.rerun()
        with nav_next:
            if st.button(
                "Next Clause",
                disabled=sel_idx >= len(clauses),
                use_container_width=True,
                key="ws_next_clause",
            ):
                st.session_state.selected_clause_idx = sel_idx + 1
                st.rerun()

        # Quick Flagged Clauses jump list
        flagged = [(i, c) for i, c in enumerate(clauses, 1) if str(c.get("risk", "")).upper() in {"HIGH", "MEDIUM"}]
        if flagged:
            st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
            render_html(
                f'<div class="cw-section-title">{lucide_icon("alert-triangle", 13)} Flagged Clauses Quick Jump</div>'
            )
            for f_idx, f_clause in flagged[:8]:
                f_risk = str(f_clause.get("risk", "MEDIUM")).upper()
                preview = clean_text(f_clause.get("simplified") or f_clause.get("original") or "")
                is_curr_jump = sel_idx == f_idx
                j_info, j_btn = st.columns([3.2, 1.0], vertical_alignment="center")
                with j_info:
                    render_html(
                        f"""
                        <div class="cw-card" style="padding:8px 11px;margin-bottom:6px;{'border-color:#5E6AD2;' if is_curr_jump else ''}">
                            <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:3px;">
                                <span class="cw-clause-id">CLAUSE {f_idx:02d}</span>
                                {risk_badge(f_risk)}
                            </div>
                            <div style="font-size:0.79rem;color:#9CA3AF;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                                {html.escape(preview)}
                            </div>
                        </div>
                        """
                    )
                with j_btn:
                    if st.button(
                        "Viewing" if is_curr_jump else "Inspect",
                        key=f"jump_flagged_{f_idx}",
                        type="primary" if is_curr_jump else "secondary",
                        use_container_width=True,
                    ):
                        st.session_state.selected_clause_idx = f_idx
                        expanded = set(st.session_state.get("expanded_clause_ids", set()))
                        expanded.add(f_idx)
                        st.session_state.expanded_clause_ids = expanded
                        st.rerun()

        # Export panel
        st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
        render_html(f'<div class="cw-section-title">{lucide_icon("download", 13)} Export Analysis</div>')
        exp_json, exp_md = st.columns(2)
        with exp_json:
            st.download_button(
                label="Download JSON",
                data=json.dumps(clauses, indent=2),
                file_name=f"clausewise_analysis_{filename}.json",
                mime="application/json",
                use_container_width=True,
                key="ws_dl_json",
            )
        with exp_md:
            st.download_button(
                label="Download Markdown",
                data=_build_markdown_report(filename, clauses, counts),
                file_name=f"clausewise_report_{filename}.md",
                mime="text/markdown",
                use_container_width=True,
                key="ws_dl_md",
            )
