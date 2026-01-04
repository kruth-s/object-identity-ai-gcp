import os
import numpy as np
import logging

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
GEMINI_LOCATION = os.environ.get("GEMINI_LOCATION", "us-central1")

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


def embed_completion_image_bytes(image_bytes: bytes) -> dict:
    """
    Returns embedding vector (list) + dims.
    """
    try:
        _init_vertex()
        model = _get_mm_model()

        from vertexai.vision_models import Image as VxImage
        vx_img = VxImage(image_bytes=image_bytes)

        emb = model.get_embeddings(image=vx_img, dimension=1408)
        vec = np.asarray(emb.image_embedding, dtype=np.float32)

        return {
            "dims": int(vec.shape[0]),
            "embedding": vec.tolist(),
        }

    except Exception as e:
        logging.exception("Completion embedding failed")
        return {"dims": 0, "embedding": [], "error": str(e)}
