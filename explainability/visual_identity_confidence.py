import numpy as np
import cv2
import logging
from google.cloud import storage

from explainability.vit_gradcam import vit_gradcam_heatmap
from explainability.heatmap_overlay import overlay_heatmap
from explainability.gemini_explanations import (
    gemini_explain_match_from_bytes,
)


def build_visual_identity_confidence(
    norm_jpg_bytes: bytes,
    bucket_name: str,
    heatmap_object_path: str,
    context_for_gemini: dict,
) -> dict:
    try:
        bgr = cv2.imdecode(
            np.frombuffer(norm_jpg_bytes, np.uint8),
            cv2.IMREAD_COLOR,
        )
        if bgr is None:
            raise ValueError("Invalid image for explainability")

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        rgb = rgb.astype(np.float32) / 255.0

        cam = vit_gradcam_heatmap(rgb)
        overlay_jpg = overlay_heatmap(rgb, cam, alpha=0.45)

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(heatmap_object_path)
        blob.upload_from_string(
            overlay_jpg,
            content_type="image/jpeg",
        )

        heatmap_gcs_uri = f"gs://{bucket_name}/{heatmap_object_path}"

        try:
            gemini_json = gemini_explain_match_from_bytes(
                norm_jpg_bytes,
                context_for_gemini,
            )
        except Exception:
            logging.warning("Gemini explainability unavailable, continuing")
            gemini_json = {
                "summary": "Explainability unavailable",
                "confidence": "low",
                "source": "fallback"
            }

        return {
            "heatmap_url": heatmap_gcs_uri,
            "gemini_explanation": gemini_json,
            "xai_notes": (
                "Grad-CAM is an approximate saliency method; "
                "explanations may vary with model and input."
            ),
            "interpretation": (
                "ViT Grad-CAM + heatmap overlay + Gemini explanation"
            ),
        }

    except Exception as e:
        logging.exception("Explainability pipeline failed")
        return {
            "heatmap_url": None,
            "gemini_explanation": {},
            "xai_notes": "",
            "interpretation": f"error: {e}",
        }
