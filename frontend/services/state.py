"""Session state management preserving existing ClauseWise keys and adding workspace history."""

from datetime import datetime
from typing import Any, Dict, Optional
import uuid

import streamlit as st

from services.api import DEFAULT_BACKEND_URL
from ui.components import compute_risk_counts


def init_session_state() -> None:
    """Initialize required session state keys safely."""
    defaults = {
        # Preserved legacy keys
        "processed_data": None,
        "uploaded_file_name": None,
        # Workspace navigation & history
        "active_page": "Overview",
        "analysis_history": [],
        "active_record_id": None,
        "selected_clause_idx": 1,
        "expanded_clause_ids": set(),
        "is_analyzing": False,
        "analysis_error": None,
        # User preferences
        "backend_url": DEFAULT_BACKEND_URL,
        "request_timeout": 300,
        "default_sort": "Document order",
        "show_inline_source": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def record_analysis_result(
    filename: str,
    file_size: int,
    data: Dict[str, Any],
    elapsed_seconds: float,
    model_name: str,
) -> str:
    """Store a completed backend analysis in session history and activate it."""
    clauses = data.get("clauses", [])
    ext = filename.rsplit(".", 1)[-1].upper() if "." in filename else "DOC"
    record_id = str(uuid.uuid4())[:8]

    record = {
        "id": record_id,
        "filename": filename,
        "file_type": ext,
        "file_size": file_size,
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "elapsed_seconds": elapsed_seconds,
        "model": model_name,
        "total_clauses": data.get("total_clauses", len(clauses)),
        "risk_counts": compute_risk_counts(clauses),
        "status": "Completed",
        "data": data,
    }

    st.session_state.analysis_history.insert(0, record)
    st.session_state.active_record_id = record_id
    st.session_state.processed_data = data
    st.session_state.uploaded_file_name = filename
    st.session_state.selected_clause_idx = 1
    st.session_state.expanded_clause_ids = (
        set(range(1, len(clauses) + 1)) if st.session_state.get("show_inline_source") else set()
    )
    return record_id


def activate_history_record(record_id: str) -> bool:
    """Load an existing session history record into the active workspace."""
    for record in st.session_state.analysis_history:
        if record["id"] == record_id:
            clauses = record["data"].get("clauses", [])
            st.session_state.active_record_id = record_id
            st.session_state.processed_data = record["data"]
            st.session_state.uploaded_file_name = record["filename"]
            st.session_state.selected_clause_idx = 1
            st.session_state.expanded_clause_ids = (
                set(range(1, len(clauses) + 1)) if st.session_state.get("show_inline_source") else set()
            )
            return True
    return False


def get_active_record() -> Optional[Dict[str, Any]]:
    """Return metadata for the currently active document if available."""
    active_id = st.session_state.get("active_record_id")
    for record in st.session_state.get("analysis_history", []):
        if record["id"] == active_id:
            return record
    return None


def delete_history_record(record_id: str) -> None:
    """Remove a record from session history and clear active view if needed."""
    st.session_state.analysis_history = [
        r for r in st.session_state.analysis_history if r["id"] != record_id
    ]
    if st.session_state.active_record_id == record_id:
        if st.session_state.analysis_history:
            activate_history_record(st.session_state.analysis_history[0]["id"])
        else:
            st.session_state.active_record_id = None
            st.session_state.processed_data = None
            st.session_state.uploaded_file_name = None
            st.session_state.selected_clause_idx = 1
