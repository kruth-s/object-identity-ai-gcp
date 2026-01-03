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

def gemini_explain_match_from_bytes(image_bytes: bytes, context: dict) -> dict:
    """
    context: fusion_result + top candidate + branch highlights
    """
    prompt = (
        "You are generating an explainable identity-confidence report.\n"
        "Return ONLY JSON:\n"
        "{"
        "\"short_reason\":\"1-2 sentences\","
        "\"key_visual_cues\":[\"...\",\"...\"],"
        "\"what_might_reduce_confidence\":[\"...\"],"
        "\"confidence_summary\":\"...\""
        "}\n"
        f"Context JSON:\n{json.dumps(context)[:1200]}"
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
            "max_output_tokens": 350,
        },
    )

    text = getattr(resp, "text", "") or ""
    m = re.search(r"(\{.*\})", text, re.S)
    if m:
        return json.loads(m.group(1))
    return json.loads(text)
