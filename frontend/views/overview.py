"""Overview dashboard view for ClauseWise."""

import html
from typing import Any, Dict, Optional

import streamlit as st

from services.state import activate_history_record
from ui.components import format_file_size, page_header, render_html
from ui.icons import lucide_icon


def render_overview(health_ok: bool, health_data: Optional[Dict[str, Any]], health_err: Optional[str]) -> None:
    """Render the clean Linear-style Workspace Overview."""
    model_name = (health_data or {}).get("model", "Unavailable")
    status_pill = (
        f'<span class="cw-pill cw-pill-low">{lucide_icon("check-circle", 12)}API Ready · {html.escape(str(model_name))}</span>'
        if health_ok
        else f'<span class="cw-pill cw-pill-high">{lucide_icon("shield-alert", 12)}Backend Offline</span>'
    )
    page_header(
        "Overview",
        "Analyze legal agreements clause by clause with verifiable passage citations.",
        badge_html=status_pill,
    )

    # Top action & status row
    col_main, col_side = st.columns([1.65, 1.0], gap="medium")

    with col_main:
        render_html(
            f"""
            <div class="cw-card cw-card-hover" style="margin-bottom:10px;">
                <div class="cw-section-title">{lucide_icon("sparkles", 13)} Start Review</div>
                <div style="font-size:1.06rem;font-weight:600;color:#F3F4F6;margin-bottom:6px;">
                    Analyze a contract or agreement
                </div>
                <p style="font-size:0.86rem;color:#9CA3AF;line-height:1.55;margin:0;">
                    Upload a PDF, DOCX, or TXT document. ClauseWise extracts individual clauses,
                    generates plain-English summaries, flags risk exposure, and links every finding
                    directly to its verbatim source text.
                </p>
            </div>
            """
        )
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("New Analysis", type="primary", use_container_width=True, key="ov_new"):
                st.session_state.active_page = "New Analysis"
                st.rerun()
        with btn_col2:
            has_active = st.session_state.processed_data is not None
            if st.button(
                "Resume Review" if has_active else "Session History",
                use_container_width=True,
                key="ov_resume",
            ):
                st.session_state.active_page = "Workspace" if has_active else "History"
                st.rerun()

    with col_side:
        dot_cls = "cw-dot-ok" if health_ok else "cw-dot-err"
        state_text = "Connected" if health_ok else f"Offline ({html.escape(health_err or 'unreachable')})"
        render_html(
            f"""
            <div class="cw-card">
                <div class="cw-section-title">{lucide_icon("activity", 13)} Engine Status</div>
                <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:7px 0;border-bottom:1px solid #22252F;">
                    <span style="font-size:0.82rem;color:#9CA3AF;white-space:nowrap;">FastAPI Backend</span>
                    <span style="font-size:0.82rem;font-weight:500;color:#F3F4F6;white-space:nowrap;"><span class="cw-dot {dot_cls}"></span>{state_text}</span>
                </div>
                <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px solid #22252F;">
                    <span style="font-size:0.82rem;color:#9CA3AF;white-space:nowrap;">Model</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.76rem;color:#D1D5DB;white-space:nowrap;">{html.escape(str(model_name))}</span>
                </div>
                <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 0 2px 0;">
                    <span style="font-size:0.82rem;color:#9CA3AF;white-space:nowrap;">Formats</span>
                    <span style="font-size:0.79rem;color:#D1D5DB;white-space:nowrap;">PDF · DOCX · TXT</span>
                </div>
            </div>
            """
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Recent session documents
    history = st.session_state.get("analysis_history", [])
    render_html(f'<div class="cw-section-title">{lucide_icon("clock", 13)} Recent Analyses (Current Session)</div>')

    if not history:
        render_html(
            f"""
            <div class="cw-card" style="padding:24px;text-align:left;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;color:#F3F4F6;font-weight:600;font-size:0.95rem;">
                    {lucide_icon("file-text", 17, "#9CA3AF")} No documents analyzed in this session yet
                </div>
                <p style="font-size:0.85rem;color:#9CA3AF;margin:0;line-height:1.55;">
                    Select <strong>New Document Analysis</strong> above to upload an NDA, employment agreement,
                    or terms of service. Analyzed documents appear here for quick switching and export.
                </p>
            </div>
            """
        )
        return

    render_html(
        """
        <div class="cw-table-wrap">
            <div class="cw-table-head">
                <div>Document</div>
                <div>Format</div>
                <div>Risk Exposure</div>
                <div>Clauses</div>
                <div>Analyzed</div>
            </div>
        </div>
        """
    )

    for rec in history[:5]:
        rc = rec["risk_counts"]
        c_row, c_btn = st.columns([5.2, 1.0], vertical_alignment="center")
        with c_row:
            render_html(
                f"""
                <div class="cw-card" style="padding:10px 14px;margin-top:6px;">
                    <div class="cw-recent-grid">
                        <div style="min-width:0;">
                            <div style="font-size:0.87rem;font-weight:500;color:#F3F4F6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                                {lucide_icon("file-check", 14, "#60A5FA")} {html.escape(rec["filename"])}
                            </div>
                            <div style="font-size:0.74rem;color:#6B7280;margin-top:2px;">{format_file_size(rec["file_size"])}</div>
                        </div>
                        <div><span class="cw-pill cw-pill-neutral">{html.escape(rec["file_type"])}</span></div>
                        <div style="display:flex;gap:6px;flex-wrap:wrap;">
                            <span class="cw-pill cw-pill-high">{rc["HIGH"]}H</span>
                            <span class="cw-pill cw-pill-medium">{rc["MEDIUM"]}M</span>
                            <span class="cw-pill cw-pill-low">{rc["LOW"]}L</span>
                        </div>
                        <div style="font-size:0.83rem;color:#D1D5DB;">{rec["total_clauses"]} clauses</div>
                        <div style="font-size:0.78rem;color:#9CA3AF;">{html.escape(rec["analyzed_at"])}</div>
                    </div>
                </div>
                """
            )
        with c_btn:
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            if st.button("Open", key=f"ov_open_{rec['id']}", use_container_width=True):
                activate_history_record(rec["id"])
                st.session_state.active_page = "Workspace"
                st.rerun()
