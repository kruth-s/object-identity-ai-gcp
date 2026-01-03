import os
import json
import re
from google import genai
from google.genai.types import HttpOptions, Part

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GEMINI_LOCATION", "asia-south1")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

_client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    http_options=HttpOptions(api_version="v1"),
)

def gemini_scene_understanding_from_bytes(image_bytes: bytes) -> dict:
    """
    Gemini Pro Vision: high-level semantics + reasoning.
    Returns JSON dict strictly shaped for Branch B.
    """
    prompt = (
        "You are an Object Identity system.\n"
        "Return ONLY valid JSON with keys exactly:\n"
        "{"
        "\"semantics\":\"...\","
        "\"object_type\":\"...\","
        "\"distinctive_marks\":\"...\","
        "\"materials\":\"...\","
        "\"scene_context\":\"...\","
        "\"lighting_notes\":\"...\","
        "\"confidence\":0.0"
        "}\n"
        "Keep each value short."
    )

    resp = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            prompt,
            Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        ],
        config={
            "response_mime_type": "application/json",
            "temperature": 0.2,
            "max_output_tokens": 300,
        },
    )

    text = getattr(resp, "text", "") or ""
    m = re.search(r"(\{.*\})", text, re.S)
    if m:
        return json.loads(m.group(1))
    return json.loads(text)

def gemini_scene_understanding_from_gcs(gcs_uri: str) -> dict:
    """Same as above but uses a gs:// URI. [web:41]"""
    prompt = (
        "Return ONLY valid JSON:\n"
        "{"
        "\"semantics\":\"...\","
        "\"object_type\":\"...\","
        "\"distinctive_marks\":\"...\","
        "\"materials\":\"...\","
        "\"scene_context\":\"...\","
        "\"lighting_notes\":\"...\","
        "\"confidence\":0.0"
        "}"
    )

    resp = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            prompt,
            Part.from_uri(file_uri=gcs_uri, mime_type="image/jpeg"),
        ],
        config={
            "response_mime_type": "application/json",
            "temperature": 0.2,
            "max_output_tokens": 300,
        },
    )

    text = getattr(resp, "text", "") or ""
    m = re.search(r"(\{.*\})", text, re.S)
    if m:
        return json.loads(m.group(1))
    return json.loads(text)
