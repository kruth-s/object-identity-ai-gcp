import numpy as np
import cv2


def _shadow_mask_score(bgr: np.ndarray) -> dict:
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    L, _, _ = cv2.split(lab)

    blur = cv2.GaussianBlur(L, (5, 5), 0)
    thr = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        51,
        2,
    )

    kernel = np.ones((5, 5), np.uint8)
    thr = cv2.morphologyEx(thr, cv2.MORPH_OPEN, kernel, iterations=1)
    thr = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, kernel, iterations=1)

    shadow_ratio = float(np.mean(thr > 0))
    return {"shadow_ratio": shadow_ratio}


def _perspective_line_cues(bgr: np.ndarray) -> dict:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 160)

    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, threshold=80, minLineLength=60, maxLineGap=10
    )

    if lines is None:
        return {"line_count": 0, "angle_hist": [0.0, 0.0, 0.0, 0.0]}

    angles = []
    for x1, y1, x2, y2 in lines[:, 0]:
        ang = np.degrees(np.arctan2((y2 - y1), (x2 - x1)))
        angles.append(ang)

    angles = np.array(angles)
    bins = [-180, -45, 0, 45, 180]
    hist, _ = np.histogram(angles, bins=bins)
    hist = (hist / max(1, hist.sum())).astype(float).tolist()

    return {"line_count": int(len(angles)), "angle_hist": hist}


def _intensity_micro_patterns(bgr: np.ndarray) -> dict:
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(gx, gy)
    energy = float(np.mean(mag))
    return {"gradient_energy": energy}


def ghost_signal_features_from_bytes(image_bytes: bytes) -> dict:
    bgr = cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR
    )
    if bgr is None:
        return {"error": "Invalid image for ghost signals", "ghost_vector": []}

    shadow = _shadow_mask_score(bgr)
    perspective = _perspective_line_cues(bgr)
    intensity = _intensity_micro_patterns(bgr)

    vector = [
        float(shadow.get("shadow_ratio", 0.0)),
        float(perspective.get("line_count", 0)),
        *perspective.get("angle_hist", [0.0, 0.0, 0.0, 0.0]),
        float(intensity.get("gradient_energy", 0.0)),
    ]

    return {
        "shadow": shadow,
        "perspective": perspective,
        "intensity": intensity,
        "ghost_vector": vector,
    }
