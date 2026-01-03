import numpy as np
import cv2

def segment_foreground_mask(norm_jpg_bytes: bytes) -> np.ndarray:
    """
    Returns binary mask (1=foreground object, 0=background).
    """
    img = cv2.imdecode(np.frombuffer(norm_jpg_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image for segmentation")

    h, w = img.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    rect = (int(w * 0.08), int(h * 0.08), int(w * 0.84), int(h * 0.84))
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 4, cv2.GC_INIT_WITH_RECT)

    fg = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    return fg
