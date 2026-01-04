import numpy as np
import logging

from fusion.schema import BranchOutput, FusionResult
from fusion.weights_store import get_branch_reliability

def _beta_from_mean_conf(mean: float, conf: float):
    import tensorflow_probability as tfp
    tfd = tfp.distributions

    mean = float(np.clip(mean, 1e-4, 1 - 1e-4))
    conf = float(np.clip(conf, 0.0, 1.0))

    total = 2.0 + conf * 50.0
    alpha = mean * total
    beta = (1.0 - mean) * total
    return tfd.Beta(concentration1=alpha, concentration0=beta)

def fuse_branch_outputs(
    branches: list[BranchOutput],
    n_samples: int = 256,
) -> FusionResult:
    try:
        reliability = get_branch_reliability()

        base = {
            "manufacturing_signature": 0.22,
            "ghost_context": 0.19,
            "partial_completion": 0.15,
            "negative_space": 0.23,
            "visual_semantics": 0.21,
        }

        raw_weights = []
        names = []

        for b in branches:
            rb = reliability.get(b.name, {"alpha": 5.0, "beta": 5.0})
            rel_mean = rb["alpha"] / (rb["alpha"] + rb["beta"])
            w = base.get(b.name, 0.2) * rel_mean * float(
                np.clip(b.confidence, 0.05, 1.0)
            )
            raw_weights.append(w)
            names.append(b.name)

        raw = np.array(raw_weights, dtype=np.float32)
        raw = raw / (raw.sum() + 1e-6)
        weights = {n: float(w) for n, w in zip(names, raw)}

        dists = [
            _beta_from_mean_conf(b.p_same_object, b.confidence)
            for b in branches
        ]

        samples = np.stack(
            [dist.sample(n_samples).numpy() for dist in dists],
            axis=1,
        )

        wvec = np.array([weights[n] for n in names], dtype=np.float32)
        post = np.sum(samples * wvec[None, :], axis=1)

        p_final = float(np.mean(post))
        low, high = np.percentile(post, [2.5, 97.5]).tolist()

        return FusionResult(
            p_final=round(p_final, 3),
            confidence_interval=[round(low, 3), round(high, 3)],
            weights={k: round(v, 3) for k, v in weights.items()},
            method="tfp_beta_bma",
        )

    except Exception as e:
        logging.exception("Fusion failed; using fallback")

        avg = float(
            np.mean([b.p_same_object for b in branches])
            if branches else 0.5
        )

        return FusionResult(
            p_final=round(avg, 3),
            confidence_interval=[round(max(0.0, avg - 0.15), 3),
                                 round(min(1.0, avg + 0.15), 3)],
            weights={b.name: round(1.0 / len(branches), 3)
                     for b in branches} if branches else {},
            method="fallback_mean",
        )
