"""Reusable global stylesheet for ClauseWise (Linear-inspired dark UI)."""

import streamlit as st

from ui.tokens import PALETTE


def inject_global_styles() -> None:
    """Inject Linear-inspired dark theme tokens, typography, spacing, and responsive rules."""
    p = PALETTE
    css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {{
    --cw-bg-canvas: {p["bg_canvas"]};
    --cw-bg-sidebar: {p["bg_sidebar"]};
    --cw-bg-surface: {p["bg_surface"]};
    --cw-bg-elevated: {p["bg_elevated"]};
    --cw-bg-hover: {p["bg_hover"]};
    --cw-border-subtle: {p["border_subtle"]};
    --cw-border-strong: {p["border_strong"]};
    --cw-text-primary: {p["text_primary"]};
    --cw-text-secondary: {p["text_secondary"]};
    --cw-text-muted: {p["text_muted"]};
    --cw-accent: {p["accent"]};
    --cw-accent-hover: {p["accent_hover"]};
    --cw-accent-soft: {p["accent_soft"]};
    --cw-accent-border: {p["accent_border"]};
    --cw-success: {p["success"]};
    --cw-warning: {p["warning"]};
    --cw-danger: {p["danger"]};
}}

/* Global typography & shell */
html, body, .stApp, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    color: var(--cw-text-primary);
}}

.stApp {{
    background-color: var(--cw-bg-canvas);
}}

/* Reduce Streamlit default chrome clutter while preserving accessible sidebar toggle */
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{
    background: rgba(10, 11, 14, 0.85);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--cw-border-subtle);
}}

[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"] button {{
    background-color: var(--cw-bg-surface) !important;
    border: 1px solid var(--cw-border-strong) !important;
    border-radius: 7px !important;
    color: var(--cw-text-primary) !important;
}}
[data-testid="stExpandSidebarButton"]:hover,
[data-testid="stSidebarCollapseButton"] button:hover {{
    background-color: var(--cw-bg-hover) !important;
    border-color: var(--cw-accent) !important;
}}

.block-container {{
    padding-top: 3.4rem;
    padding-bottom: 3rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1380px;
}}

/* Sidebar shell */
section[data-testid="stSidebar"] {{
    background-color: var(--cw-bg-sidebar) !important;
    border-right: 1px solid var(--cw-border-subtle);
}}
section[data-testid="stSidebar"] .block-container {{
    padding-top: 0.75rem;
    padding-left: 1rem;
    padding-right: 1rem;
}}

/* Sidebar nav buttons — crisp left-aligned Linear rows */
section[data-testid="stSidebar"] div.stButton > button {{
    width: 100%;
    justify-content: flex-start !important;
    text-align: left !important;
    background: transparent;
    border: 1px solid transparent;
    color: var(--cw-text-secondary);
    border-radius: 7px;
    padding: 0.45rem 0.75rem;
    min-height: 36px;
    font-size: 0.86rem;
    font-weight: 500;
    transition: background-color 140ms ease, color 140ms ease, border-color 140ms ease;
    box-shadow: none;
}}
section[data-testid="stSidebar"] div.stButton > button > div,
section[data-testid="stSidebar"] div.stButton > button p {{
    width: 100%;
    text-align: left !important;
    justify-content: flex-start !important;
    margin: 0 !important;
}}
section[data-testid="stSidebar"] div.stButton > button:hover {{
    background: var(--cw-bg-hover);
    color: var(--cw-text-primary);
    border-color: var(--cw-border-subtle);
}}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {{
    background: var(--cw-bg-elevated);
    color: var(--cw-text-primary);
    border: 1px solid var(--cw-border-strong);
    border-left: 2px solid var(--cw-accent);
}}

/* Main buttons */
.stApp div.stButton > button,
.stApp div.stDownloadButton > button {{
    min-height: 38px;
    max-width: 100%;
    overflow: hidden;
    border-radius: 7px;
    font-size: 0.855rem;
    font-weight: 500;
    padding: 0.4rem 0.85rem;
    border: 1px solid var(--cw-border-strong);
    background-color: var(--cw-bg-surface);
    color: var(--cw-text-primary);
    transition: background-color 140ms ease, border-color 140ms ease;
}}
.stApp div.stButton > button > div,
.stApp div.stButton > button p,
.stApp div.stDownloadButton > button > div,
.stApp div.stDownloadButton > button p {{
    min-width: 0;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin: 0 !important;
}}
.stApp div.stButton > button:hover,
.stApp div.stDownloadButton > button:hover {{
    background-color: var(--cw-bg-hover);
    border-color: #3E4354;
}}
.stApp div.stButton > button[kind="primary"] {{
    background-color: var(--cw-accent);
    border-color: var(--cw-accent);
    color: #FFFFFF;
}}
.stApp div.stButton > button[kind="primary"]:hover {{
    background-color: var(--cw-accent-hover);
    border-color: var(--cw-accent-hover);
}}
.stApp div.stButton > button:disabled,
.stApp div.stButton > button[disabled],
.stApp div.stButton > button[kind="primary"]:disabled {{
    background-color: var(--cw-bg-elevated) !important;
    border-color: var(--cw-border-subtle) !important;
    color: var(--cw-text-muted) !important;
    opacity: 0.65 !important;
    cursor: not-allowed !important;
}}

/* Inputs & Selectboxes */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
textarea {{
    background-color: var(--cw-bg-surface) !important;
    border: 1px solid var(--cw-border-subtle) !important;
    border-radius: 7px !important;
    color: var(--cw-text-primary) !important;
    min-height: 38px;
}}
div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {{
    border-color: var(--cw-accent) !important;
}}

/* File uploader polish */
section[data-testid="stFileUploaderDropzone"] {{
    background-color: var(--cw-bg-surface) !important;
    border: 1px dashed var(--cw-border-strong) !important;
    border-radius: 10px !important;
    padding: 1.5rem 1.25rem !important;
    transition: border-color 150ms ease, background-color 150ms ease;
}}
section[data-testid="stFileUploaderDropzone"]:hover {{
    border-color: var(--cw-accent) !important;
    background-color: var(--cw-bg-elevated) !important;
}}

/* Custom ClauseWise surface classes */
.cw-topbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 8px 0 14px 0;
    margin-bottom: 14px;
    border-bottom: 1px solid var(--cw-border-subtle);
}}
.cw-topbar-brand {{
    display: flex;
    align-items: center;
    gap: 11px;
}}
.cw-topbar-title {{
    font-size: 1.05rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--cw-text-primary);
    line-height: 1.1;
}}
.cw-topbar-sub {{
    font-size: 0.74rem;
    color: var(--cw-text-muted);
    margin-top: 2px;
}}
.cw-brand-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 6px 14px 6px;
    border-bottom: 1px solid var(--cw-border-subtle);
    margin-bottom: 12px;
}}
.cw-brand-mark {{
    width: 28px;
    height: 28px;
    border-radius: 7px;
    background: var(--cw-accent-soft);
    border: 1px solid var(--cw-accent-border);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: #8E9AFF;
}}
.cw-brand-name {{
    font-size: 0.96rem;
    font-weight: 600;
    letter-spacing: -0.015em;
    color: var(--cw-text-primary);
    line-height: 1.1;
}}
.cw-brand-sub {{
    font-size: 0.72rem;
    color: var(--cw-text-muted);
    margin-top: 2px;
}}

.cw-nav-group-label {{
    font-size: 0.69rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--cw-text-muted);
    padding: 10px 6px 6px 6px;
}}

.cw-page-header {{
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
    justify-content: space-between;
    gap: 12px;
    padding-bottom: 16px;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--cw-border-subtle);
}}
.cw-page-title {{
    font-size: 1.45rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--cw-text-primary);
    margin: 0;
    line-height: 1.25;
}}
.cw-page-desc {{
    font-size: 0.875rem;
    color: var(--cw-text-secondary);
    margin: 4px 0 0 0;
}}

.cw-card {{
    background: var(--cw-bg-surface);
    border: 1px solid var(--cw-border-subtle);
    border-radius: 10px;
    padding: 16px 18px;
    transition: border-color 140ms ease;
}}
.cw-card-hover:hover {{
    border-color: var(--cw-border-strong);
}}

.cw-section-title {{
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--cw-text-muted);
    margin: 0 0 10px 0;
}}

/* Badges */
.cw-pill {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    white-space: nowrap;
}}
.cw-pill-high {{
    background: {p["danger_soft"]};
    color: #FCA5A5;
    border: 1px solid {p["danger_border"]};
}}
.cw-pill-medium {{
    background: {p["warning_soft"]};
    color: #FCD34D;
    border: 1px solid {p["warning_border"]};
}}
.cw-pill-low {{
    background: {p["success_soft"]};
    color: #86EFAC;
    border: 1px solid {p["success_border"]};
}}
.cw-pill-neutral {{
    background: rgba(255, 255, 255, 0.04);
    color: var(--cw-text-secondary);
    border: 1px solid var(--cw-border-subtle);
}}
.cw-pill-accent {{
    background: var(--cw-accent-soft);
    color: #A5B4FC;
    border: 1px solid var(--cw-accent-border);
}}

/* AI finding vs Document fact distinction */
.cw-clause-shell {{
    background: var(--cw-bg-surface);
    border: 1px solid var(--cw-border-subtle);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 12px;
    animation: cwFadeIn 180ms ease-out;
}}
.cw-clause-shell.cw-clause-active {{
    border-color: var(--cw-accent);
    background: #161822;
}}
.cw-clause-meta {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding-bottom: 10px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--cw-border-subtle);
}}
.cw-clause-id {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--cw-text-secondary);
}}
.cw-ai-block {{
    margin-bottom: 12px;
}}
.cw-block-tag {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.70rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #93A1F8;
    margin-bottom: 5px;
}}
.cw-fact-tag {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.70rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--cw-text-muted);
    margin-bottom: 6px;
}}
.cw-ai-summary {{
    font-size: 0.935rem;
    line-height: 1.62;
    color: var(--cw-text-primary);
}}
.cw-ai-rationale {{
    background: var(--cw-bg-elevated);
    border: 1px solid var(--cw-border-subtle);
    border-left: 2px solid var(--cw-accent);
    border-radius: 6px;
    padding: 10px 12px;
    font-size: 0.855rem;
    line-height: 1.55;
    color: #D1D5DB;
    margin-bottom: 10px;
}}
.cw-source-panel {{
    background: #0D0E12;
    border: 1px solid var(--cw-border-subtle);
    border-radius: 10px;
    padding: 16px 18px;
}}
.cw-source-passage {{
    background: #08090C;
    border: 1px solid var(--cw-border-subtle);
    border-radius: 7px;
    padding: 14px;
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 0.81rem;
    line-height: 1.65;
    color: #CBD5E1;
    white-space: pre-wrap;
    word-break: break-word;
}}
.cw-kw-mark {{
    background: rgba(245, 158, 11, 0.18);
    color: #FCD34D;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid rgba(245, 158, 11, 0.30);
}}

/* History & data table */
.cw-table-wrap {{
    background: var(--cw-bg-surface);
    border: 1px solid var(--cw-border-subtle);
    border-radius: 10px;
    overflow: hidden;
}}
.cw-table-head, .cw-table-row, .cw-recent-grid {{
    display: grid;
    grid-template-columns: 2.2fr 0.7fr 1.2fr 0.9fr 1.1fr;
    gap: 12px;
    align-items: center;
}}
.cw-table-head, .cw-table-row {{
    padding: 10px 16px;
}}
.cw-table-head {{
    background: var(--cw-bg-elevated);
    border-bottom: 1px solid var(--cw-border-subtle);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--cw-text-muted);
}}
.cw-table-row {{
    border-bottom: 1px solid var(--cw-border-subtle);
    font-size: 0.86rem;
    color: var(--cw-text-primary);
}}
.cw-table-row:last-child {{
    border-bottom: none;
}}

/* Status dot */
.cw-status-box {{
    background: var(--cw-bg-surface);
    border: 1px solid var(--cw-border-subtle);
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 0.80rem;
}}
.cw-dot {{
    width: 7px;
    height: 7px;
    border-radius: 999px;
    display: inline-block;
    margin-right: 6px;
}}
.cw-dot-ok {{ background: var(--cw-success); }}
.cw-dot-err {{ background: var(--cw-danger); }}

/* Inline details fallback */
.cw-inline-details summary {{
    cursor: pointer;
    font-size: 0.82rem;
    font-weight: 500;
    color: #93A1F8;
    list-style: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}}
.cw-inline-details summary:hover {{
    text-decoration: underline;
}}

@keyframes cwFadeIn {{
    from {{ opacity: 0; transform: translateY(3px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Responsive adjustments */
@media (max-width: 992px) {{
    .block-container {{
        padding-left: 1.1rem;
        padding-right: 1.1rem;
    }}
    .cw-table-head {{
        display: none;
    }}
    .cw-table-row, .cw-recent-grid {{
        grid-template-columns: 1fr !important;
        gap: 6px;
    }}
}}

@media (max-width: 640px) {{
    .block-container {{
        padding-top: 1.5rem;
        padding-left: 0.85rem;
        padding-right: 0.85rem;
    }}
    .cw-page-title {{
        font-size: 1.22rem;
    }}
}}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)
