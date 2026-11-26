"""Backend API client preserving exact backend endpoints and upload semantics."""

import os
import time
from typing import Any, Dict, Optional, Tuple

import requests

DEFAULT_BACKEND_URL = os.getenv("CLAUSEWISE_BACKEND_URL", "http://127.0.0.1:8000")


def check_health(backend_url: str = DEFAULT_BACKEND_URL, timeout: int = 5) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Query GET /health and return (ok, payload, error_message)."""
    try:
        response = requests.get(f"{backend_url.rstrip('/')}/health", timeout=timeout)
        if response.status_code == 200:
            return True, response.json(), None
        return False, None, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, None, "Backend unreachable"
    except requests.exceptions.Timeout:
        return False, None, "Health check timed out"
    except Exception as exc:
        return False, None, str(exc)


def analyze_document(
    uploaded_file: Any,
    backend_url: str = DEFAULT_BACKEND_URL,
    timeout: int = 300,
) -> Tuple[Optional[Dict[str, Any]], Optional[str], float]:
    """Send document to POST /analyze and return (response_json, error_message, elapsed_seconds)."""
    started = time.perf_counter()
    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        mime_type = getattr(uploaded_file, "type", None) or "application/octet-stream"
        files = {"file": (uploaded_file.name, uploaded_file, mime_type)}
        response = requests.post(
            f"{backend_url.rstrip('/')}/analyze",
            files=files,
            timeout=timeout,
        )
        elapsed = round(time.perf_counter() - started, 2)
        if response.status_code == 200:
            return response.json(), None, elapsed
        detail = response.text
        try:
            parsed = response.json()
            if isinstance(parsed, dict) and "detail" in parsed:
                detail = str(parsed["detail"])
        except ValueError:
            pass
        return None, f"Analysis failed ({response.status_code}): {detail}", elapsed
    except requests.exceptions.ConnectionError:
        return (
            None,
            f"Cannot connect to backend at {backend_url}. Start the FastAPI server and try again.",
            round(time.perf_counter() - started, 2),
        )
    except requests.exceptions.Timeout:
        return (
            None,
            "Request timed out while waiting for document analysis. Try increasing the timeout in Settings.",
            round(time.perf_counter() - started, 2),
        )
    except Exception as exc:
        return None, f"Unexpected error: {str(exc)}", round(time.perf_counter() - started, 2)
