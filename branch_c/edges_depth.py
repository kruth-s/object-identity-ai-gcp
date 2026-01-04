import numpy as np
import cv2


def edge_map_bytes(image_bytes: bytes) -> bytes:
    bgr = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("Invalid image for edges")

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 160)

    ok, png = cv2.imencode(".png", edges)
    if not ok:
        raise RuntimeError("Edge map encode failed")
    return png.tobytes()


def depth_prior_bytes(image_bytes: bytes) -> bytes:
    """
    Cheap depth prior: radial gradient (center=near).
    """
    bgr = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("Invalid image for depth prior")

    h, w = bgr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cy, cx = h / 2.0, w / 2.0
    dist = np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2)
    dist = dist / (dist.max() + 1e-6)

    depth = ((1.0 - dist) * 255.0).astype(np.uint8)

    ok, png = cv2.imencode(".png", depth)
    if not ok:
        raise RuntimeError("Depth prior encode failed")
    return png.tobytes()
