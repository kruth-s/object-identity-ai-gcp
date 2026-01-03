import cv2
import numpy as np

def normalize_image(data: bytes) -> bytes:
    """Resize + CLAHE + Color Constancy (Section 1 of Pipeline)."""
    # 1. Decode
    arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image data")

    # 2. Resize (max 768px, keep aspect)
    h, w = img.shape[:2]
    max_side = 768
    scale = min(max_side / max(h, w), 1.0)
    if scale < 1.0:
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    # 3. CLAHE + Color Constancy (LAB space)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    limg = cv2.merge((l, a, b))
    img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # 4. Encode back to bytes
    _, buf = cv2.imencode(".jpg", img)
    return buf.tobytes()
