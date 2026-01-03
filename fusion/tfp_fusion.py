import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

from fusion.schema import BranchOutput, FusionResult
from fusion.weights_store import get_branch_reliability

tfd = tfp.distributions

def _beta_from_mean_conf(mean: float, conf: float):
    """
    Convert (mean, confidence) -> Beta(alpha,beta)
    Higher confidence => higher concentration => lower variance.
    """
    mean = float(np.clip(mean, 1e-4, 1 - 1e-4))
    conf = float(np.clip(conf, 0.0, 1.0))

    # concentration in [2, 52] (tuneable)
    total = 2.0 + conf * 50.0
    alpha = mean * total
    beta = (1.0 - mean) * total
    return tfd.Beta(concentration1=alpha, concentration0=beta)

def fuse_branch_outputs(branches: list[BranchOutput], n_samples: int = 256) -> FusionResult:
    """
    Bayesian model averaging over branch distributions.
    Returns posterior mean + 95% interval + dynamic weights.
    """
    reliability = get_branch_reliability()

    # 1) Compute reliability mean weight per branch from stored Beta(alpha,beta)
    rel_weights = {}
    for b in branches:
        rb = reliability.get(b.name, {"alpha": 5.0, "beta": 5.0})
        rel_mean = rb["alpha"] / (rb["alpha"] + rb["beta"])
        rel_weights[b.name] = float(rel_mean)

    # 2) Base weights (from your slide)
    base = {
        "manufacturing_signature": 0.22,
        "ghost_context": 0.19,
        "partial_completion": 0.15,
        "negative_space": 0.23,
        "visual_semantics": 0.21,
    }

    # 3) Dynamic weight = base * reliability_mean * branch_confidence
    raw = []
    names = []
    for b in branches:
        w = base.get(b.name, 0.2) * rel_weights.get(b.name, 0.5) * float(np.clip(b.confidence, 0.05, 1.0))
        raw.append(w)
        names.append(b.name)

    raw = np.array(raw, dtype=np.float32)
    raw = raw / raw.sum()

    weights = {n: float(w) for n, w in zip(names, raw)}

    # 4) Sample each branch Beta, weighted sum => posterior samples
    dists = [_beta_from_mean_conf(b.p_same_object, b.confidence) for b in branches]
    samples = [dist.sample(n_samples).numpy() for dist in dists]  # shape [n_samples]
    samples = np.stack(samples, axis=1)                           # [n_samples, n_branches]

    wvec = np.array([weights[n] for n in names], dtype=np.float32)
    post = np.sum(samples * wvec[None, :], axis=1)                # [n_samples]

    p_final = float(np.mean(post))
    low, high = np.percentile(post, [2.5, 97.5]).tolist()

    return FusionResult(
        p_final=round(p_final, 3),
        confidence_interval=[round(low, 3), round(high, 3)],
        weights={k: round(v, 3) for k, v in weights.items()},
        method="tfp_beta_bma",
    )
