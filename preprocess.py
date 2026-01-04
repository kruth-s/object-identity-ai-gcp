import cv2
import numpy as np
import logging


def normalize_image(data: bytes) -> bytes:
    """
    Image normalization pipeline:
    1) Decode
    2) Resize (max side 768px, preserve aspect)
    3) CLAHE on luminance (LAB) for illumination robustness
    4) Encode back to JPEG bytes
    """
    try:
        # 1. Decode
        arr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image data")

        # 2. Resize
        h, w = img.shape[:2]
        max_side = 768
        scale = min(max_side / max(h, w), 1.0)
        if scale < 1.0:
            img = cv2.resize(
                img,
                (int(w * scale), int(h * scale)),
                interpolation=cv2.INTER_AREA,
            )

        # 3. CLAHE in LAB space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8),
        )
        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # 4. Encode
        ok, buf = cv2.imencode(
            ".jpg",
            img,
            [int(cv2.IMWRITE_JPEG_QUALITY), 92],
        )
        if not ok:
            raise RuntimeError("Failed to encode normalized image")

        return buf.tobytes()

    except Exception:
        logging.exception("Image normalization failed")
        raise
