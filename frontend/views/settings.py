"""Settings view for ClauseWise."""

import html
import time
import streamlit as st

from services.api import DEFAULT_BACKEND_URL, check_health
from ui.components import page_header, render_html
from ui.icons import lucide_icon


def render_settings() -> None:
    """Render functional backend, workspace, and session settings."""
    page_header(
        "Settings",
        "Configure backend connection parameters, workspace review defaults, and session storage.",
    )

    col_left, col_right = st.columns([1.3, 1.0], gap="large")

    with col_left:
        render_html(f'<div class="cw-section-title">{lucide_icon("activity", 13)} Backend Connection</div>')

        backend_url = st.text_input(
            "FastAPI Backend URL",
            value=st.session_state.backend_url,
            help="Base URL for the ClauseWise FastAPI server (default: http://127.0.0.1:8000).",
            key="set_backend_url",
        )
        timeout = st.number_input(
            "Analysis Request Timeout (seconds)",
            min_value=30,
            max_value=600,
            value=int(st.session_state.request_timeout),
            step=30,
            help="Maximum time to wait for POST /analyze on large documents.",
            key="set_timeout",
        )

        b1, b2 = st.columns(2)
        with b1:
            if st.button("Save Connection Settings", type="primary", use_container_width=True, key="set_save_conn"):
                st.session_state.backend_url = backend_url.strip() or DEFAULT_BACKEND_URL
                st.session_state.request_timeout = int(timeout)
                st.success("Connection settings saved for this session.")
        with b2:
            if st.button("Test Backend Health", use_container_width=True, key="set_test_health"):
                target = backend_url.strip() or DEFAULT_BACKEND_URL
                t0 = time.perf_counter()
                ok, payload, err = check_health(target)
                ms = round((time.perf_counter() - t0) * 1000)
                if ok:
                    model = (payload or {}).get("model", "unknown")
                    st.success(f"Connected ({ms} ms) — model: {model}")
                else:
                    st.error(f"Health check failed: {err}")

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
        render_html(f'<div class="cw-section-title">{lucide_icon("settings", 13)} Review Preferences</div>')

        default_sort = st.selectbox(
            "Default clause order in Workspace",
            ["Document order", "Highest risk first"],
            index=0 if st.session_state.default_sort == "Document order" else 1,
            key="set_sort",
        )
        show_inline = st.checkbox(
            "Expand all source citations inline by default",
            value=bool(st.session_state.show_inline_source),
            key="set_inline",
        )
        if st.button("Apply Review Preferences", use_container_width=True, key="set_save_prefs"):
            st.session_state.default_sort = default_sort
            st.session_state.show_inline_source = show_inline
            st.success("Review preferences updated.")

    with col_right:
        count = len(st.session_state.get("analysis_history", []))
        render_html(
            f"""
            <div class="cw-card">
                <div class="cw-section-title">{lucide_icon("history", 13)} Session Data</div>
                <p style="font-size:0.85rem;color:#9CA3AF;line-height:1.55;margin:0 0 12px 0;">
                    ClauseWise currently holds <strong style="color:#F3F4F6;">{count}</strong> analyzed
                    document(s) in browser session memory. Uploaded files are deleted from backend
                    temporary storage immediately after analysis.
                </p>
                <div style="font-size:0.78rem;color:#6B7280;">
                    Active endpoint: <code>{html.escape(st.session_state.backend_url)}</code>
                </div>
            </div>
            """
        )
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button(
            "Clear Session History",
            disabled=count == 0,
            use_container_width=True,
            key="set_clear_hist",
        ):
            st.session_state.analysis_history = []
            st.session_state.active_record_id = None
            st.session_state.processed_data = None
            st.session_state.uploaded_file_name = None
            st.session_state.selected_clause_idx = 1
            st.success("Session history cleared.")
            st.rerun()
