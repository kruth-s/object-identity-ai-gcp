import numpy as np

def cosine_sim(a: list, b: list) -> float:
    if not a or not b:
        return 0.0

    va = np.asarray(a, dtype=np.float32)
    vb = np.asarray(b, dtype=np.float32)

    if va.size == 0 or vb.size == 0:
        return 0.0

    na = np.linalg.norm(va) + 1e-6
    nb = np.linalg.norm(vb) + 1e-6

    return float(np.dot(va, vb) / (na * nb))

def blend_similarity(scores: dict, weights: dict) -> float:
    num = 0.0
    den = 0.0

    for k, s in scores.items():
        w = float(weights.get(k, 0.0))
        if w <= 0.0:
            continue
        num += w * float(s)
        den += w

    return float(num / (den + 1e-6))
