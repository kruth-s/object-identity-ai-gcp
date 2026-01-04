import os
import json
import re
import logging
import google.auth
from google import genai
from google.genai.types import Part

# -------------------------------------------------------------------
# Environment
# -------------------------------------------------------------------

def get_project_id():
    # 1. Explicit env var (preferred)
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        return project_id
    
    # 2. Default credentials fallback
    try:
        _, project_id = google.auth.default()
        if project_id:
            return project_id
    except Exception as e:
        logging.warning(f"Gemini project detection failed: {e}")
    
    # 3. Non-fatal fallback
    logging.warning("Gemini running without explicit project_id")
    return None

PROJECT_ID = get_project_id()
GEMINI_LOCATION = os.environ.get("GEMINI_LOCATION", "asia-south1")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# -------------------------------------------------------------------
# Lazy Gemini client (Cloud Run safe)
# -------------------------------------------------------------------

_client = None

def _get_client():
    global _client
    if _client is None:
        if not PROJECT_ID:
            raise RuntimeError("Cannot init Gemini: No PROJECT_ID found")
        
        _client = genai.Client(
            vertexai=True,
            project=PROJECT_ID,
            location=GEMINI_LOCATION,
        )
    return _client

# -------------------------------------------------------------------
# Robust JSON parsing (MANDATORY)
# -------------------------------------------------------------------

def _safe_json_parse(text: str) -> dict:
    if not text:
        return {
            "semantics": "",
            "object_type": "object",
            "distinctive_marks": "",
            "materials": "",
            "scene_context": "",
            "lighting_notes": "",
            "confidence": 0.5,
        }

    # 1️⃣ Direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # 2️⃣ Extract first JSON block (non-greedy)
    match = re.search(r"\{[\s\S]*?\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass

    # 3️⃣ Hard fallback (never crash)
    logging.warning("Gemini returned malformed JSON, using fallback")
    return {
        "semantics": "",
        "object_type": "object",
        "distinctive_marks": "",
        "materials": "",
        "scene_context": "",
        "lighting_notes": "",
        "confidence": 0.5,
    }

# -------------------------------------------------------------------
# Gemini Vision – BYTES
# -------------------------------------------------------------------

def gemini_scene_understanding_from_bytes(image_bytes: bytes) -> dict:
    if not PROJECT_ID:
        return {
            "semantics": "",
            "object_type": "object",
            "distinctive_marks": "",
            "materials": "",
            "scene_context": "",
            "lighting_notes": "",
            "confidence": 0.0,
            "interpretation": "Gemini unavailable (no project)",
            "source": "disabled"
        }

    try:
        client = _get_client()

        prompt = (
            "Analyze the image and return ONLY valid JSON with keys:\n"
            "{"
            "\"semantics\":\"\","
            "\"object_type\":\"\","
            "\"distinctive_marks\":\"\","
            "\"materials\":\"\","
            "\"scene_context\":\"\","
            "\"lighting_notes\":\"\","
            "\"confidence\":0.0"
            "}"
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/jpeg",
                ),
                prompt,
            ],
            config={
                "temperature": 0.2,
                "max_output_tokens": 300,
            },
        )

        text = getattr(response, "text", "") or ""
        return _safe_json_parse(text)

    except Exception as e:
        logging.exception("Gemini bytes vision failed")
        return {
            "semantics": "",
            "object_type": "object",
            "distinctive_marks": "",
            "materials": "",
            "scene_context": "",
            "lighting_notes": "",
            "confidence": 0.0,
            "error": str(e),
        }

# -------------------------------------------------------------------
# Gemini Vision – GCS URI
# -------------------------------------------------------------------

def gemini_scene_understanding_from_gcs(gcs_uri: str) -> dict:
    try:
        client = _get_client()

        prompt = (
            "Analyze the image and return ONLY valid JSON:\n"
            "{"
            "\"semantics\":\"\","
            "\"object_type\":\"\","
            "\"distinctive_marks\":\"\","
            "\"materials\":\"\","
            "\"scene_context\":\"\","
            "\"lighting_notes\":\"\","
            "\"confidence\":0.0"
            "}"
        )

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                Part.from_uri(
                    file_uri=gcs_uri,
                    mime_type="image/jpeg",
                ),
                prompt,
            ],
            config={
                "temperature": 0.2,
                "max_output_tokens": 300,
            },
        )

        text = getattr(response, "text", "") or ""
        return _safe_json_parse(text)

    except Exception as e:
        logging.exception("Gemini GCS vision failed")
        return {
            "semantics": "",
            "object_type": "object",
            "distinctive_marks": "",
            "materials": "",
            "scene_context": "",
            "lighting_notes": "",
            "confidence": 0.0,
            "error": str(e),
        }
