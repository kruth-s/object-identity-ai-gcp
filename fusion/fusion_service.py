from fusion.schema import BranchOutput
from fusion.tfp_fusion import fuse_branch_outputs

def run_fusion(branches_dict: dict) -> dict:
    outputs = []

    for name, payload in branches_dict.items():
        conf = float(payload.get("confidence", 0.5))
        p = float(payload.get("p_same_object", conf))
        outputs.append(
            BranchOutput(
                name=name,
                p_same_object=p,
                confidence=conf,
            )
        )

    result = fuse_branch_outputs(outputs, n_samples=256)

    ci = result.confidence_interval
    uncertainty = "low" if (ci[1] - ci[0]) < 0.2 else "high"

    return {
        "probability_same_object": result.p_final,
        "confidence_score": result.p_final,
        "confidence_interval": ci,
        "branch_weights": result.weights,
        "uncertainty_level": uncertainty,
        "method": result.method,
    }
