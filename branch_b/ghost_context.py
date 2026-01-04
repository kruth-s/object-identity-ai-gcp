import numpy as np

from branch_b.gemini_vision import gemini_scene_understanding_from_bytes
from branch_b.mediapipe_geometry import mediapipe_geometry_from_bytes
from branch_b.ghost_signals import ghost_signal_features_from_bytes


def build_ghost_context_embedding(norm_bytes: bytes) -> dict:
    # Run sub-branches defensively
    gemini = gemini_scene_understanding_from_bytes(norm_bytes) or {}
    mp_geo = mediapipe_geometry_from_bytes(norm_bytes) or {}
    ghost = ghost_signal_features_from_bytes(norm_bytes) or {}

    # Geometry vector (always fixed length)
    geo_vec = [
        1.0 if mp_geo.get("has_face") else 0.0,
        1.0 if mp_geo.get("has_pose") else 0.0,
        1.0 if mp_geo.get("has_left_hand") else 0.0,
        1.0 if mp_geo.get("has_right_hand") else 0.0,
        float(mp_geo.get("human_interaction_score", 0.0)),
    ]

    ghost_vec = ghost.get("ghost_vector", [])
    if not isinstance(ghost_vec, list):
        ghost_vec = []

    full_vec = np.array(geo_vec + ghost_vec, dtype=np.float32)

    # Confidence heuristic (bounded, stable)
    confidence = float(
        min(
            1.0,
            0.55
            + 0.25 * float(mp_geo.get("human_interaction_score", 0.0))
            + 0.2 * (1.0 - float(ghost.get("shadow", {}).get("shadow_ratio", 0.0))),
        )
    )

    return {
        "confidence": round(confidence, 3),
        "semantics": gemini.get("semantics", ""),
        "semantic_class": gemini.get(
            "object_type", gemini.get("semantic_class", "object")
        ),
        "ghost_signals": {
            "gemini": gemini,
            "mediapipe": mp_geo,
            "custom": ghost,
        },
        "ghost_context_embedding": full_vec.tolist(),
        "interpretation": (
            "Gemini Vision + MediaPipe geometry + custom ghost signals fused"
        ),
    }
