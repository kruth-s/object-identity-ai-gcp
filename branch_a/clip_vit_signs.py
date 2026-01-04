import torch
import timm
import numpy as np
import hashlib
import io
import logging
from PIL import Image

# -------------------------------------------------------------------
# Cloud Run SAFE settings
# -------------------------------------------------------------------

_DEVICE = torch.device("cpu")  # FORCE CPU (Cloud Run safe)

_clip_model = None
_clip_preprocess = None
_manuf_model = None

# -------------------------------------------------------------------
# Lazy model loaders
# -------------------------------------------------------------------

def _load_clip():
    global _clip_model, _clip_preprocess
    if _clip_model is None:
        import clip
        logging.info("Loading CLIP ViT-B/32 (CPU)")
        _clip_model, _clip_preprocess = clip.load(
            "ViT-B/32",
            device=_DEVICE,
            jit=False,
        )
        _clip_model.eval()
    return _clip_model, _clip_preprocess


def _load_manuf_vit():
    global _manuf_model
    if _manuf_model is None:
        logging.info("Loading ViT-Base for manufacturing signature (CPU)")
        _manuf_model = timm.create_model(
            "vit_base_patch16_224",
            pretrained=True,
            num_classes=0,
        )
        _manuf_model.eval()
        _manuf_model.to(_DEVICE)
    return _manuf_model

# -------------------------------------------------------------------
# Utility
# -------------------------------------------------------------------

def _load_image_from_bytes(image_bytes: bytes) -> Image.Image:
    return Image.open(io.BytesIO(image_bytes)).convert("RGB")

# -------------------------------------------------------------------
# Branch A1 — CLIP semantic embedding
# -------------------------------------------------------------------

def get_clip_embedding_bytes(image_bytes: bytes) -> list:
    """
    CLIP semantic embedding (512D).
    """
    try:
        clip_model, preprocess = _load_clip()
        image = _load_image_from_bytes(image_bytes)
        image_input = preprocess(image).unsqueeze(0).to(_DEVICE)

        with torch.no_grad():
            emb = clip_model.encode_image(image_input)
            emb = emb / (emb.norm(dim=-1, keepdim=True) + 1e-6)

        return emb.cpu().numpy().flatten().tolist()

    except Exception as e:
        logging.exception("CLIP embedding failed")
        return []

# -------------------------------------------------------------------
# Branch A2 — Manufacturing signature (ViT patch variance)
# -------------------------------------------------------------------

def get_manufacturing_signature_bytes(image_bytes: bytes) -> dict:
    """
    Latent manufacturing fingerprint via ViT patch variance.
    """
    try:
        model = _load_manuf_vit()
        image = _load_image_from_bytes(image_bytes).resize((224, 224))

        img_tensor = (
            torch.tensor(np.array(image))
            .permute(2, 0, 1)
            .unsqueeze(0)
            .float()
            / 255.0
        ).to(_DEVICE)

        with torch.no_grad():
            features = model.forward_features(img_tensor)

        patch_embeddings = features[:, 1:, :]  # drop CLS
        signature = torch.var(patch_embeddings, dim=1)
        signature_np = signature.cpu().numpy().flatten()

        fingerprint_id = hashlib.md5(
            signature_np.tobytes()
        ).hexdigest()[:10]

        patch_inconsistency = float(np.mean(signature_np))

        return {
            "fingerprint_id": f"mfg_{fingerprint_id}",
            "patch_inconsistency_score": round(patch_inconsistency, 6),
            "confidence": round(
                float(1.0 - min(patch_inconsistency * 10.0, 1.0)), 3
            ),
            "signature_dim": int(signature_np.shape[0]),
            "interpretation": (
                "ViT-Base patch variance manufacturing signature"
            ),
        }

    except Exception as e:
        logging.exception("Manufacturing signature failed")
        return {
            "fingerprint_id": None,
            "patch_inconsistency_score": 0.0,
            "confidence": 0.0,
            "signature_dim": 0,
            "interpretation": f"error: {e}",
        }

# -------------------------------------------------------------------
# Unified processor
# -------------------------------------------------------------------

def process_image_bytes(image_bytes: bytes) -> dict:
    """
    Unified Branch A output.
    """
    return {
        "clip_embedding": get_clip_embedding_bytes(image_bytes),
        "manufacturing_signature": get_manufacturing_signature_bytes(image_bytes),
    }
