import os
import json
import re
import logging
from google import genai
from google.genai.types import Part

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
GEMINI_LOCATION = os.environ.get("GEMINI_LOCATION", "asia-south1")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=GEMINI_LOCATION,
        )
    return _client


def _safe_json_parse(text: str) -> dict:
    if not text or not text.strip():
        return {
            "summary": "No LLM explanation available",
            "confidence": "low",
            "reasoning": [],
            "source": "fallback"
        }

    # direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # extract {...}
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    logging.warning("Gemini returned malformed JSON")
    return {
        "short_reason": "Explanation unavailable",
        "key_visual_cues": [],
        "what_might_reduce_confidence": [],
        "confidence_summary": "Gemini formatting issue",
    }


def gemini_explain_match_from_bytes(image_bytes: bytes, context: dict) -> dict:
    client = _get_client()

    prompt = (
        "You are generating an explainable identity-confidence report.\n"
        "Return ONLY valid JSON:\n"
        "{"
        "\"short_reason\":\"...\","
        "\"key_visual_cues\":[\"...\"],"
        "\"what_might_reduce_confidence\":[\"...\"],"
        "\"confidence_summary\":\"...\""
        "}\n\n"
        f"Context:\n{json.dumps(context)[:1200]}"
    )

    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            prompt,
            Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg",
            ),
        ],
        config={  # ✅ THIS IS CORRECT
            "response_mime_type": "application/json",
            "temperature": 0.2,
            "max_output_tokens": 350,
        },
    )

    text = getattr(resp, "text", "") or ""
    return _safe_json_parse(text)
