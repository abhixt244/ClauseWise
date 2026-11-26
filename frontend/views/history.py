"""Session Document History view for ClauseWise."""

import html
import json
import streamlit as st

from services.state import activate_history_record, delete_history_record
from ui.components import format_file_size, page_header, render_html
from ui.icons import lucide_icon


def render_history() -> None:
    """Render the clean Linear-style Document History table."""
    history = st.session_state.get("analysis_history", [])
    badge = f'<span class="cw-pill cw-pill-neutral">{lucide_icon("history", 12)}{len(history)} in session</span>'
    page_header(
        "Document History",
        "Documents analyzed during this browser session. Re-open any report or export JSON.",
        badge_html=badge,
    )

    if not history:
        render_html(
            f"""
            <div class="cw-card" style="padding:28px;max-width:660px;">
                <div style="display:flex;align-items:center;gap:10px;color:#F3F4F6;font-weight:600;margin-bottom:6px;">
                    {lucide_icon("history", 17, "#9CA3AF")} No analysis history yet
                </div>
                <p style="font-size:0.86rem;color:#9CA3AF;margin:0;line-height:1.55;">
                    ClauseWise processes documents statelessly on the backend and keeps analyzed results
                    in your active browser session. Analyze a document to track it here.
                </p>
            </div>
            """
        )
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        if st.button("New Analysis", type="primary", key="hist_empty_new"):
            st.session_state.active_page = "New Analysis"
            st.rerun()
        return

    # Search and format filter bar
    f1, f2 = st.columns([2.2, 1.0])
    with f1:
        query = st.text_input(
            "Search history",
            placeholder="Filter by document name...",
            label_visibility="collapsed",
            key="hist_search",
        ).strip().lower()
    with f2:
        fmt_filter = st.selectbox(
            "Format",
            ["All Formats", "PDF", "DOCX", "TXT"],
            label_visibility="collapsed",
            key="hist_fmt",
        )

    filtered = [
        rec
        for rec in history
        if (not query or query in rec["filename"].lower())
        and (fmt_filter == "All Formats" or rec["file_type"] == fmt_filter)
    ]

    st.caption(f"Showing {len(filtered)} of {len(history)} documents")

    render_html(
        """
        <div class="cw-table-wrap">
            <div class="cw-table-head">
                <div>Document</div>
                <div>Type</div>
                <div>Risk Exposure</div>
                <div>Clauses</div>
                <div>Status &amp; Time</div>
            </div>
        </div>
        """
    )

    active_id = st.session_state.get("active_record_id")
    for rec in filtered:
        rc = rec["risk_counts"]
        is_active = rec["id"] == active_id
        active_tag = '<span class="cw-pill cw-pill-accent">Active</span>' if is_active else ""

        col_info, col_open, col_dl, col_del = st.columns([4.6, 0.75, 0.75, 0.65], vertical_alignment="center")
        with col_info:
            render_html(
                f"""
                <div class="cw-card" style="padding:10px 14px;margin-top:6px;">
                    <div class="cw-recent-grid">
                        <div style="min-width:0;">
                            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                                <span style="font-size:0.87rem;font-weight:500;color:#F3F4F6;word-break:break-word;">
                                    {html.escape(rec["filename"])}
                                </span>
                                {active_tag}
                            </div>
                            <div style="font-size:0.74rem;color:#6B7280;margin-top:2px;">
                                {format_file_size(rec["file_size"])} · {rec["elapsed_seconds"]}s
                            </div>
                        </div>
                        <div><span class="cw-pill cw-pill-neutral">{html.escape(rec["file_type"])}</span></div>
                        <div style="display:flex;gap:5px;flex-wrap:wrap;">
                            <span class="cw-pill cw-pill-high">{rc["HIGH"]}H</span>
                            <span class="cw-pill cw-pill-medium">{rc["MEDIUM"]}M</span>
                            <span class="cw-pill cw-pill-low">{rc["LOW"]}L</span>
                        </div>
                        <div style="font-size:0.83rem;color:#D1D5DB;">{rec["total_clauses"]} clauses</div>
                        <div style="font-size:0.78rem;color:#9CA3AF;">{html.escape(rec["status"])} · {html.escape(rec["analyzed_at"])}</div>
                    </div>
                </div>
                """
            )
        with col_open:
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            if st.button("Open", key=f"h_open_{rec['id']}", use_container_width=True):
                activate_history_record(rec["id"])
                st.session_state.active_page = "Workspace"
                st.rerun()
        with col_dl:
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            st.download_button(
                label="JSON",
                data=json.dumps(rec["data"].get("clauses", []), indent=2),
                file_name=f"clausewise_analysis_{rec['filename']}.json",
                mime="application/json",
                key=f"h_dl_{rec['id']}",
                use_container_width=True,
            )
        with col_del:
            st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
            if st.button("Remove", key=f"h_del_{rec['id']}", use_container_width=True):
                delete_history_record(rec["id"])
                st.rerun()
