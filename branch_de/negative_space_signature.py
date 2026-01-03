import numpy as np
import cv2

def edge_irregularity_score(fg_mask: np.ndarray) -> float:
    """
    Circularity-based irregularity: higher = more jagged boundary.
    """
    fg = (fg_mask * 255).astype(np.uint8)
    contours, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return 1.5

    c = max(contours, key=cv2.contourArea)
    perim = cv2.arcLength(c, True)
    area = cv2.contourArea(c)
    circularity = 4 * np.pi * area / (perim * perim + 1e-6)
    return float(1.0 / max(circularity, 1e-6))

def find_void_regions(fg_mask: np.ndarray):
    """
    Voids = background pixels inside the object region.
    Approx: fill object hull, subtract fg.
    """
    fg = (fg_mask * 255).astype(np.uint8)

    contours, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return [], np.zeros_like(fg)

    c = max(contours, key=cv2.contourArea)

    hull = cv2.convexHull(c)
    filled = np.zeros_like(fg)
    cv2.drawContours(filled, [hull], -1, 255, thickness=-1)

    void_mask = cv2.subtract(filled, fg)  # inside hull but not in fg

    # connected components = void regions
    n, labels, stats, centroids = cv2.connectedComponentsWithStats(void_mask)
    voids = []
    for i in range(1, n):  # skip background
        x, y, w, h, area = stats[i]
        if area < 100:  # ignore tiny noise
            continue
        cx, cy = centroids[i]
        voids.append({
            "bbox": [int(x), int(y), int(x+w), int(y+h)],
            "area": int(area),
            "centroid": [float(cx), float(cy)]
        })

    return voids, void_mask

def negative_space_signature_128(voids: list, edge_irreg: float) -> list:
    """
    Build a 128D signature from void statistics:
    - 64 bins: void area histogram (log-scaled)
    - 32 bins: void centroid radial histogram
    - 32 bins: edge irregularity repeated/smoothed (cheap stable filler)
    """
    # --- area histogram (64) ---
    areas = np.array([v["area"] for v in voids], dtype=np.float32)
    if areas.size == 0:
        area_hist = np.zeros(64, dtype=np.float32)
    else:
        la = np.log1p(areas)
        area_hist, _ = np.histogram(la, bins=64, range=(0.0, float(max(1.0, la.max()))))
        area_hist = area_hist.astype(np.float32)
        area_hist = area_hist / (area_hist.sum() + 1e-6)

    # --- centroid radial histogram (32) ---
    if len(voids) == 0:
        rad_hist = np.zeros(32, dtype=np.float32)
    else:
        cxy = np.array([v["centroid"] for v in voids], dtype=np.float32)
        # normalize to [0..1] with respect to bounding box of centroids
        minxy = cxy.min(axis=0)
        maxxy = cxy.max(axis=0)
        denom = (maxxy - minxy) + 1e-6
        norm = (cxy - minxy) / denom
        r = np.sqrt((norm[:, 0] - 0.5) ** 2 + (norm[:, 1] - 0.5) ** 2)
        rad_hist, _ = np.histogram(r, bins=32, range=(0.0, 1.0))
        rad_hist = rad_hist.astype(np.float32)
        rad_hist = rad_hist / (rad_hist.sum() + 1e-6)

    # --- edge irregularity block (32) ---
    edge_block = np.full(32, float(edge_irreg), dtype=np.float32)
    edge_block = edge_block / (edge_block.max() + 1e-6)

    sig = np.concatenate([area_hist, rad_hist, edge_block], axis=0)
    assert sig.shape[0] == 128
    return sig.tolist()
