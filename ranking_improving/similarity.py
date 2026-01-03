import numpy as np

def cosine_sim(a: list, b: list) -> float:
    va = np.array(a, dtype=np.float32)
    vb = np.array(b, dtype=np.float32)
    na = np.linalg.norm(va) + 1e-6
    nb = np.linalg.norm(vb) + 1e-6
    return float(np.dot(va, vb) / (na * nb))

def blend_similarity(scores: dict, weights: dict) -> float:
    """
    scores = {"semantic":0.8, "negative":0.6, "mfg":0.7}
    weights = {"semantic":0.6, "negative":0.3, "mfg":0.1}
    """
    num = 0.0
    den = 0.0
    for k, s in scores.items():
        w = float(weights.get(k, 0.0))
        num += w * float(s)
        den += w
    return float(num / (den + 1e-6))
