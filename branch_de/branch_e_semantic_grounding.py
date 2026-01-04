import os
import numpy as np
import logging
import google.auth

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
        logging.warning(f"Branch E project detection failed: {e}")
    
    # 3. Non-fatal fallback
    logging.warning("Branch E running without explicit project_id")
    return None

PROJECT_ID = get_project_id()
GEMINI_LOCATION = os.environ.get("GEMINI_LOCATION", "us-central1")

# -------------------------------------------------------------------
# Lazy Vertex AI globals
# -------------------------------------------------------------------

_vertex_initialized = False
_mm_model = None

def _init_vertex():
    global _vertex_initialized
    if not _vertex_initialized:
        import vertexai
        vertexai.init(project=PROJECT_ID, location=GEMINI_LOCATION)
        _vertex_initialized = True

def _get_mm_model():
    global _mm_model
    if _mm_model is None:
        from vertexai.vision_models import MultiModalEmbeddingModel
        _mm_model = MultiModalEmbeddingModel.from_pretrained(
            "multimodalembedding@001"
        )
    return _mm_model

# -------------------------------------------------------------------
# Branch E — Semantic grounding (SAFE)
# -------------------------------------------------------------------

def run_branch_e_semantics_from_gcs(
    gcs_uri: str,
    contextual_text: str = ""
) -> dict:
    if not PROJECT_ID:
        return {
            "confidence": 0.0,
            "semantic_embedding_dims": 0,
            "semantic_embedding": [],
            "interpretation": "Branch E unavailable (no project)",
        }

    try:
        _init_vertex()
        model = _get_mm_model()

        from vertexai.vision_models import Image

        img = Image.load_from_file(gcs_uri)
        emb = model.get_embeddings(
            image=img,
            contextual_text=contextual_text,
            dimension=1408,
        )

        vec = np.asarray(emb.image_embedding, dtype=np.float32)

        return {
            "confidence": 0.92,
            "semantic_embedding_dims": int(vec.shape[0]),
            "semantic_embedding": vec.tolist(),
            "interpretation": (
                "Vertex AI multimodalembedding@001 global embedding"
            ),
        }

    except Exception as e:
        logging.exception("Branch E semantic grounding failed")
        return {
            "confidence": 0.0,
            "semantic_embedding_dims": 0,
            "semantic_embedding": [],
            "interpretation": f"error: {e}",
        }
