import numpy as np
import cv2
import logging


def segment_foreground_mask(norm_jpg_bytes: bytes) -> np.ndarray:
    """
    Returns binary mask (1=foreground object, 0=background).
    Safe GrabCut with fallback.
    """
    img = cv2.imdecode(
        np.frombuffer(norm_jpg_bytes, np.uint8), cv2.IMREAD_COLOR
    )
    if img is None:
        raise ValueError("Invalid image for segmentation")

    h, w = img.shape[:2]

    try:
        mask = np.zeros((h, w), np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        rect = (
            int(w * 0.08),
            int(h * 0.08),
            int(w * 0.84),
            int(h * 0.84),
        )

        cv2.grabCut(
            img, mask, rect, bgdModel, fgdModel, 4, cv2.GC_INIT_WITH_RECT
        )

        fg = np.where(
            (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0
        ).astype("uint8")
        return fg

    except Exception:
        logging.exception("GrabCut failed; using fallback segmentation")

        # Fallback: simple central foreground
        fg = np.zeros((h, w), dtype="uint8")
        fg[int(h * 0.15): int(h * 0.85), int(w * 0.15): int(w * 0.85)] = 1
        return fg
