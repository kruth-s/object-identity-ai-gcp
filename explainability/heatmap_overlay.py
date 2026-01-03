import numpy as np
import cv2

def overlay_heatmap(rgb_float01: np.ndarray, grayscale_cam: np.ndarray, alpha: float = 0.45) -> bytes:
    """
    Returns JPG bytes of overlay visualization.
    """
    h, w = rgb_float01.shape[:2]
    cam = cv2.resize(grayscale_cam, (w, h))
    cam = np.clip(cam, 0.0, 1.0)

    heatmap = cv2.applyColorMap((cam * 255).astype(np.uint8), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0

    overlay = (1 - alpha) * rgb_float01 + alpha * heatmap
    overlay = np.clip(overlay, 0.0, 1.0)

    overlay_bgr = cv2.cvtColor((overlay * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    ok, jpg = cv2.imencode(".jpg", overlay_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    if not ok:
        raise RuntimeError("Failed to encode heatmap overlay")
    return jpg.tobytes()
