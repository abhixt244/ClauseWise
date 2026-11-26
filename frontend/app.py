"""ClauseWise — Application shell and view router."""

import html
import os
import sys

import streamlit as st

# Ensure local imports resolve cleanly regardless of launch working directory
_FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
if _FRONTEND_DIR not in sys.path:
    sys.path.insert(0, _FRONTEND_DIR)

from services.api import check_health
from services.state import activate_history_record, init_session_state
from ui.components import render_html
from ui.icons import clausewise_logo_mark, lucide_icon
from ui.styles import inject_global_styles
from views.history import render_history
from views.overview import render_overview
from views.settings import render_settings
from views.upload import render_upload
from views.workspace import render_workspace

_LOGO_SVG_PATH = os.path.join(_FRONTEND_DIR, "assets", "logo.svg")
_LOGO_ICON_PATH = os.path.join(_FRONTEND_DIR, "assets", "logo_icon.svg")

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="ClauseWise — Legal Document AI",
    page_icon=_LOGO_ICON_PATH if os.path.exists(_LOGO_ICON_PATH) else "⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if hasattr(st, "logo") and os.path.exists(_LOGO_SVG_PATH):
    st.logo(
        _LOGO_SVG_PATH,
        size="large",
        icon_image=_LOGO_ICON_PATH if os.path.exists(_LOGO_ICON_PATH) else None,
    )

inject_global_styles()
init_session_state()

# Check live backend health
health_ok, health_data, health_err = check_health(st.session_state.backend_url, timeout=3)
active_model = (health_data or {}).get("model", "gemini-3.5-flash-lite")


def _nav_button(label: str, page_key: str, key_suffix: str) -> None:
    is_active = st.session_state.active_page == page_key
    if st.button(
        label,
        key=f"nav_{key_suffix}",
        type="primary" if is_active else "secondary",
        use_container_width=True,
    ):
        st.session_state.active_page = page_key
        st.rerun()


# ============================================
# SIDEBAR SHELL
# ============================================
with st.sidebar:
    render_html('<div class="cw-nav-group-label" style="padding-top:2px;">Workspace</div>')
    _nav_button("Overview", "Overview", "overview")
    _nav_button("New Analysis", "New Analysis", "new_analysis")
    _nav_button("Review Workspace", "Workspace", "workspace")
    _nav_button("History", "History", "history")

    render_html('<div class="cw-nav-group-label">System</div>')
    _nav_button("Settings", "Settings", "settings")

    history = st.session_state.get("analysis_history", [])
    if history:
        render_html('<div class="cw-nav-group-label">Session Documents</div>')
        active_id = st.session_state.get("active_record_id")
        for rec in history[:4]:
            name = rec["filename"]
            short_name = name if len(name) <= 24 else name[:21] + "..."
            is_curr = rec["id"] == active_id and st.session_state.active_page == "Workspace"
            if st.button(
                short_name,
                key=f"sb_doc_{rec['id']}",
                type="primary" if is_curr else "secondary",
                use_container_width=True,
            ):
                activate_history_record(rec["id"])
                st.session_state.active_page = "Workspace"
                st.rerun()

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    dot_cls = "cw-dot-ok" if health_ok else "cw-dot-err"
    status_label = "Backend connected" if health_ok else "Backend offline"
    model_line = (
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.72rem;color:#6B7280;margin-top:4px;">{html.escape(str(active_model))}</div>'
        if health_ok
        else f'<div style="font-size:0.72rem;color:#9CA3AF;margin-top:4px;">{html.escape(health_err or "Check Settings")}</div>'
    )
    render_html(
        f"""
        <div class="cw-status-box">
            <div style="color:#E5E7EB;font-weight:500;">
                <span class="cw-dot {dot_cls}"></span>{status_label}
            </div>
            {model_line}
        </div>
        """
    )

# ============================================
# PERSISTENT PROJECT TITLE & LOGO BAR
# ============================================
top_dot = "cw-dot-ok" if health_ok else "cw-dot-err"
top_status = "API Online" if health_ok else "API Offline"
render_html(
    f"""
    <div class="cw-topbar">
        <div class="cw-topbar-brand">
            {clausewise_logo_mark(32)}
            <div>
                <div class="cw-topbar-title">ClauseWise</div>
                <div class="cw-topbar-sub">Legal Document Intelligence &amp; Clause Review</div>
            </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            <span class="cw-pill cw-pill-neutral"><span class="cw-dot {top_dot}"></span>{top_status}</span>
            <span class="cw-pill cw-pill-accent">{html.escape(st.session_state.active_page)}</span>
        </div>
    </div>
    """
)

# ============================================
# PAGE ROUTER
# ============================================
page = st.session_state.active_page

if page == "Overview":
    render_overview(health_ok, health_data, health_err)
elif page == "New Analysis":
    render_upload(health_ok, active_model)
elif page == "Workspace":
    render_workspace()
elif page == "History":
    render_history()
elif page == "Settings":
    render_settings()
else:
    render_overview(health_ok, health_data, health_err)

# ============================================
# QUIET LEGAL DISCLAIMER FOOTER
# ============================================
render_html(
    """
    <div style="border-top:1px solid #22252F;margin-top:36px;padding-top:14px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;font-size:0.76rem;color:#6B7280;">
        <span>ClauseWise · Legal Document Analysis</span>
        <span>Informational review only — consult qualified legal counsel for legal advice.</span>
    </div>
    """
)
