import html
import json
import os
import re
import time

import requests

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODELS = list(dict.fromkeys([
    MODEL_NAME,
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
]))
API_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
API_REVISION = "2026-05-20"
TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "original": {"type": "string"},
        "simplified": {"type": "string"},
        "risk": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
        "reason": {"type": "string"},
    },
    "required": ["original", "simplified", "risk", "reason"],
}


def strip_html_tags(text: str) -> str:
    clean = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(clean)).strip()


def _extract_output_text(interaction: dict) -> str:
    text_parts = []
    for step in interaction.get("steps", []):
        if step.get("type") != "model_output":
            continue
        for item in step.get("content", []):
            if item.get("type") == "text":
                text_parts.append(item.get("text", ""))
    return "".join(text_parts).strip()


def _request_interaction(api_key: str, model_name: str, clause: str) -> dict:
    payload = {
        "model": model_name,
        "system_instruction": (
            "Analyze legal clauses for informational purposes, not as legal advice. "
            "Explain the clause in plain English, classify risk as HIGH, MEDIUM, or LOW, "
            "and cite specific wording in the reason. Return only the requested JSON."
        ),
        "input": f"Analyze this legal clause:\n\n{clause}",
        "response_format": {
            "type": "text",
            "mime_type": "application/json",
            "schema": RESPONSE_SCHEMA,
        },
    }

    response = None
    last_exc = None
    for attempt in range(2):
        try:
            response = requests.post(
                API_URL,
                headers={
                    "x-goog-api-key": api_key,
                    "Content-Type": "application/json",
                    "Api-Revision": API_REVISION,
                },
                json=payload,
                timeout=90,
            )
            if response.status_code in TRANSIENT_STATUS_CODES and attempt == 0:
                time.sleep(1.5)
                continue
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            last_exc = exc
            if attempt == 0 and (response is None or response.status_code in TRANSIENT_STATUS_CODES):
                time.sleep(1.5)
                continue
            detail = response.text if response is not None else str(exc)
            raise RuntimeError(f"Gemini API request failed ({model_name}): {detail}") from exc
        except ValueError as exc:
            raise RuntimeError(f"Gemini API returned an invalid JSON response ({model_name}).") from exc

    raise RuntimeError(f"Gemini API request failed ({model_name}): {last_exc}")


def call_gemini(clause: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Set it in the backend terminal before starting the server."
        )

    interaction = None
    last_error = None
    for model_name in FALLBACK_MODELS:
        try:
            interaction = _request_interaction(api_key, model_name, clause)
            break
        except RuntimeError as exc:
            last_error = exc
            print(f"   ⚠️  {exc}")

    if interaction is None:
        raise last_error or RuntimeError("Gemini API request failed across all models.")

    output_text = _extract_output_text(interaction)
    if not output_text:
        raise RuntimeError("Gemini API returned no text for the clause analysis.")

    try:
        result = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini API returned malformed analysis JSON.") from exc

    if not isinstance(result, dict):
        raise RuntimeError("Gemini API analysis must be a JSON object.")

    required_fields = ("simplified", "risk", "reason")
    if any(not isinstance(result.get(field), str) for field in required_fields):
        raise RuntimeError("Gemini API analysis is missing required text fields.")

    risk = result["risk"].upper().strip()
    if risk not in {"HIGH", "MEDIUM", "LOW"}:
        raise RuntimeError("Gemini API returned an unsupported risk classification.")

    return True, {
        "original": clause,
        "simplified": strip_html_tags(result["simplified"]),
        "risk": risk,
        "reason": strip_html_tags(result["reason"]),
    }
