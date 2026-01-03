import numpy as np
import cv2
from google.cloud import storage

from explainability.vit_gradcam import vit_gradcam_heatmap
from explainability.heatmap_overlay import overlay_heatmap
from explainability.gemini_explanations import gemini_explain_match_from_bytes

def build_visual_identity_confidence(
    norm_jpg_bytes: bytes,
    bucket_name: str,
    heatmap_object_path: str,
    context_for_gemini: dict,
) -> dict:
    """
    - Generates ViT Grad-CAM heatmap
    - Overlays onto image
    - Uploads heatmap JPG to GCS
    - Gets Gemini explanation (JSON)
    """
    # decode to RGB float
    bgr = cv2.imdecode(np.frombuffer(norm_jpg_bytes, np.uint8), cv2.IMREAD_COLOR)
    if bgr is None:
        return {"error": "invalid_image_for_explainability"}

    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0

    cam = vit_gradcam_heatmap(rgb)
    overlay_jpg = overlay_heatmap(rgb, cam, alpha=0.45)

    # upload heatmap to GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(heatmap_object_path)
    blob.upload_from_string(overlay_jpg, content_type="image/jpeg")

    heatmap_gcs_uri = f"gs://{bucket_name}/{heatmap_object_path}"

    # gemini narrative
    gemini_json = gemini_explain_match_from_bytes(norm_jpg_bytes, context_for_gemini)

    return {
        "heatmap_url": heatmap_gcs_uri,
        "gemini_explanation": gemini_json,
        "xai_notes": (
            "Grad-CAM is an approximate saliency method; explanations depend on model/data and can vary with settings."
        ),
        "interpretation": "ViT Grad-CAM + heatmap overlay + Gemini explanation",
    }
