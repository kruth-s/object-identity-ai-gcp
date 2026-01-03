import torch
import clip
import timm
import numpy as np
import hashlib
import io
import logging
from PIL import Image

# -------------------------------------------------------------------
# Device Detection (Cloud Run = CPU, Local / GPU if available)
# -------------------------------------------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Loading models on device: {device}")

# -------------------------------------------------------------------
# 1. Load CLIP (Semantic Branch)
# -------------------------------------------------------------------
clip_model, clip_preprocess = clip.load("ViT-L/14", device=device)
clip_model.eval()

# -------------------------------------------------------------------
# 2. Load ViT (Manufacturing Signature Branch)
# -------------------------------------------------------------------
manuf_model = timm.create_model(
    "vit_base_patch16_224",
    pretrained=True,
    num_classes=0  # important: we want embeddings, not classifier
)
manuf_model.eval()
manuf_model.to(device)

# -------------------------------------------------------------------
# Utility: Load image from bytes
# -------------------------------------------------------------------
def _load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")

# -------------------------------------------------------------------
# Branch E — CLIP Semantic Embedding
# -------------------------------------------------------------------
def get_clip_embedding_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Generate CLIP embedding for semantic similarity matching.
    Output: (768,) or (1024,) depending on CLIP variant
    """
    image = _load_image_from_bytes(image_bytes)
    image_input = clip_preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        embedding = clip_model.encode_image(image_input)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)

    return embedding.cpu().numpy().flatten()

# -------------------------------------------------------------------
# Branch A — Manufacturing Signature (Patch Variance)
# -------------------------------------------------------------------
def get_manufacturing_signature_bytes(image_bytes: bytes) -> dict:
    """
    Extract latent manufacturing noise using ViT patch variance.
    This acts as a quasi-fingerprint for object identity.
    """
    image = _load_image_from_bytes(image_bytes)
    image = image.resize((224, 224))

    img_tensor = (
        torch.tensor(np.array(image))
        .permute(2, 0, 1)
        .unsqueeze(0)
        .float() / 255.0
    ).to(device)

    with torch.no_grad():
        features = manuf_model.forward_features(img_tensor)

    # Remove CLS token → (1, num_patches, dim)
    patch_embeddings = features[:, 1:, :]

    # Patch variance = manufacturing noise signature
    signature = torch.var(patch_embeddings, dim=1)
    signature_np = signature.cpu().numpy().flatten()

    # Stable fingerprint ID
    fingerprint_id = hashlib.md5(signature_np.tobytes()).hexdigest()[:10]

    # Inconsistency score
    patch_inconsistency = float(np.mean(signature_np))

    return {
        "fingerprint_id": f"mfg_{fingerprint_id}",
        "patch_inconsistency_score": patch_inconsistency,
        "confidence": float(1.0 - min(patch_inconsistency * 10.0, 1.0)),
        "signature_dim": signature_np.shape[0],
        "interpretation": "ViT-Base Patch Variance Manufacturing Signature"
    }

# -------------------------------------------------------------------
# Unified Processor (Recommended API Entry)
# -------------------------------------------------------------------
def process_image_bytes(image_bytes: bytes) -> dict:
    """
    Full multi-branch processing for one image.
    Returns all signals needed by downstream ranking / graph logic.
    """
    return {
        "clip_embedding": get_clip_embedding_bytes(image_bytes),
        "manufacturing_signature": get_manufacturing_signature_bytes(image_bytes),
    }
