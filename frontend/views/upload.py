"""Document Upload & Analysis view for ClauseWise."""

import html
import streamlit as st

from services.api import analyze_document
from services.state import record_analysis_result
from ui.components import format_file_size, page_header, render_html
from ui.icons import lucide_icon


def _trigger_analysis() -> None:
    """Lock the Analyze button immediately via session state before processing begins."""
    st.session_state.is_analyzing = True
    st.session_state.analysis_error = None


def render_upload(health_ok: bool, model_name: str) -> None:
    """Render the New Analysis document upload experience."""
    format_badge = f'<span class="cw-pill cw-pill-neutral">{lucide_icon("file-text", 12)}PDF · DOCX · TXT</span>'
    page_header(
        "New Analysis",
        "Upload a legal document to extract clauses, summarize obligations, and assess risk.",
        badge_html=format_badge,
    )

    if not health_ok:
        st.warning(
            "Backend server appears offline. Verify the FastAPI server is running or update the endpoint in Settings."
        )

    col_upload, col_guide = st.columns([1.6, 1.0], gap="large")

    with col_upload:
        render_html(
            f"""
            <div class="cw-section-title">{lucide_icon("upload-cloud", 13)} Document Upload</div>
            """
        )

        is_busy = bool(st.session_state.get("is_analyzing", False))

        uploaded_file = st.file_uploader(
            "Drag and drop a contract or browse files",
            type=["pdf", "docx", "txt"],
            help="Supported backend formats: PDF (.pdf), Word (.docx), and UTF-8 plain text (.txt).",
            disabled=is_busy,
            key="cw_file_uploader",
        )

        if uploaded_file is not None:
            ext = uploaded_file.name.rsplit(".", 1)[-1].upper() if "." in uploaded_file.name else "FILE"
            render_html(
                f"""
                <div class="cw-card" style="margin-top:10px;margin-bottom:14px;">
                    <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
                        <div style="display:flex;align-items:center;gap:10px;min-width:0;">
                            <span style="color:#60A5FA;">{lucide_icon("file-check", 18)}</span>
                            <div style="min-width:0;">
                                <div style="font-size:0.90rem;font-weight:600;color:#F3F4F6;word-break:break-word;">
                                    {html.escape(uploaded_file.name)}
                                </div>
                                <div style="font-size:0.77rem;color:#9CA3AF;margin-top:2px;">
                                    {"Analyzing document..." if is_busy else f"Ready for extraction · {format_file_size(uploaded_file.size)}"}
                                </div>
                            </div>
                        </div>
                        <span class="cw-pill cw-pill-accent">{html.escape(ext)}</span>
                    </div>
                </div>
                """
            )

            st.button(
                "Analyzing Document..." if is_busy else "Analyze Document",
                type="primary",
                use_container_width=True,
                disabled=(not health_ok) or is_busy,
                on_click=_trigger_analysis,
                key="cw_run_analysis_btn",
            )

            if st.session_state.get("analysis_error") and not is_busy:
                st.error(st.session_state.analysis_error)

            if is_busy:
                backend_url = st.session_state.backend_url
                timeout = int(st.session_state.request_timeout)
                try:
                    with st.status("Processing document on ClauseWise backend...", expanded=True) as status:
                        st.write("1. Uploading file and extracting raw text...")
                        st.write("2. Segmenting clauses and querying Gemini API...")
                        result, error, elapsed = analyze_document(
                            uploaded_file,
                            backend_url=backend_url,
                            timeout=timeout,
                        )
                        if error:
                            status.update(label="Analysis failed", state="error", expanded=True)
                            st.session_state.analysis_error = error
                        elif result and result.get("success"):
                            status.update(
                                label=f"Completed {result.get('total_clauses', 0)} clauses in {elapsed}s",
                                state="complete",
                                expanded=False,
                            )
                            st.session_state.is_analyzing = False
                            st.session_state.analysis_error = None
                            record_analysis_result(
                                filename=uploaded_file.name,
                                file_size=uploaded_file.size,
                                data=result,
                                elapsed_seconds=elapsed,
                                model_name=model_name,
                            )
                            st.session_state.active_page = "Workspace"
                            st.rerun()
                        else:
                            status.update(label="Analysis returned an empty response", state="error", expanded=True)
                            st.session_state.analysis_error = "Analysis failed. Check backend logs and try again."
                finally:
                    st.session_state.is_analyzing = False
                if st.session_state.get("analysis_error"):
                    st.rerun()
        else:
            st.session_state.is_analyzing = False
            st.session_state.analysis_error = None
            render_html(
                """
                <div class="cw-card" style="margin-top:10px;border-style:dashed;">
                    <div style="font-size:0.86rem;color:#9CA3AF;line-height:1.55;">
                        Select a <strong style="color:#F3F4F6;">.pdf</strong>, <strong style="color:#F3F4F6;">.docx</strong>,
                        or <strong style="color:#F3F4F6;">.txt</strong> file above to preview file details and start clause review.
                    </div>
                </div>
                """
            )

    with col_guide:
        render_html(
            f"""
            <div class="cw-card">
                <div class="cw-section-title">{lucide_icon("book-open", 13)} Analysis Pipeline</div>
                <div style="display:flex;flex-direction:column;gap:12px;">
                    <div style="padding-bottom:10px;border-bottom:1px solid #22252F;">
                        <div style="font-size:0.84rem;font-weight:600;color:#F3F4F6;">1. Text Extraction</div>
                        <div style="font-size:0.80rem;color:#9CA3AF;margin-top:3px;line-height:1.45;">
                            Parses text from PDF pages, Word paragraphs, or plain UTF-8 files without retaining uploads on disk.
                        </div>
                    </div>
                    <div style="padding-bottom:10px;border-bottom:1px solid #22252F;">
                        <div style="font-size:0.84rem;font-weight:600;color:#F3F4F6;">2. Clause Segmentation</div>
                        <div style="font-size:0.80rem;color:#9CA3AF;margin-top:3px;line-height:1.45;">
                            Detects section headings, numbered articles, and sentence boundaries (10–150 words per segment).
                        </div>
                    </div>
                    <div>
                        <div style="font-size:0.84rem;font-weight:600;color:#F3F4F6;">3. Hybrid Risk &amp; Simplification</div>
                        <div style="font-size:0.80rem;color:#9CA3AF;margin-top:3px;line-height:1.45;">
                            Generates plain-English summaries via Gemini and cross-checks against legal risk keywords.
                        </div>
                    </div>
                </div>
            </div>
            """
        )
