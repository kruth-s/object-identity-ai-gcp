import os
import numpy as np
import vertexai
from vertexai.vision_models import Image as VxImage, MultiModalEmbeddingModel

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GEMINI_LOCATION", "asia-south1")

vertexai.init(project=PROJECT_ID, location=LOCATION)
_mm = MultiModalEmbeddingModel.from_pretrained("multimodalembedding@001")

def embed_completion_image_bytes(image_bytes: bytes) -> dict:
    """
    Returns embedding vector (list) + dims.
    """
    vx_img = VxImage(image_bytes=image_bytes)
    emb = _mm.get_embeddings(image=vx_img, dimension=1408)
    vec = np.array(emb.image_embedding, dtype=np.float32)
    return {"dims": int(vec.shape[0]), "embedding": vec.tolist()}
