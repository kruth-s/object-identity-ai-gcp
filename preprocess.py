import cv2
import numpy as np
import logging
import hashlib
from typing import Tuple


def normalize_image(
    data: bytes,
    max_side: int = 768,
) -> Tuple[bytes, dict]:
    """
    Identity-safe image normalization.

    Returns:
        normalized_image_bytes
        normalization_metadata
    """

    try:
        # -------------------------
        # 1. Decode
        # -------------------------
        arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid image bytes")

        orig_h, orig_w = img.shape[:2]

        # -------------------------
        # 2. Resize (preserve aspect)
        # -------------------------
        scale = min(max_side / max(orig_h, orig_w), 1.0)
        if scale < 1.0:
            img = cv2.resize(
                img,
                (int(orig_w * scale), int(orig_h * scale)),
                interpolation=cv2.INTER_AREA,
            )

        # -------------------------
        # 3. Color constancy (Gray World)
        # -------------------------
        img_float = img.astype(np.float32)
        avg_bgr = np.mean(img_float, axis=(0, 1))
        gray_value = np.mean(avg_bgr)

        img_float *= (gray_value / (avg_bgr + 1e-6))
        img_float = np.clip(img_float, 0, 255).astype(np.uint8)

        # -------------------------
        # 4. CLAHE on luminance
        # -------------------------
        lab = cv2.cvtColor(img_float, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8),
        )
        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))
        img_norm = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # -------------------------
        # 5. Encode (high-quality JPEG)
        # -------------------------
        ok, buf = cv2.imencode(
            ".jpg",
            img_norm,
            [int(cv2.IMWRITE_JPEG_QUALITY), 92],
        )
        if not ok:
            raise RuntimeError("Encoding failed")

        normalized_bytes = buf.tobytes()

        # -------------------------
        # 6. Deterministic hash (identity-safe)
        # -------------------------
        image_hash = hashlib.sha256(normalized_bytes).hexdigest()

        metadata = {
            "original_size": [orig_w, orig_h],
            "normalized_size": img_norm.shape[:2][::-1],
            "scale": scale,
            "hash": image_hash,
            "clahe": True,
            "color_constancy": "gray_world",
        }

        return normalized_bytes, metadata

    except Exception as e:
        logging.exception("Normalization failed")
        raise
